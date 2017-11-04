
# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

# !/usr/bin/env python3


import logging
import sys
import time

import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import meraki_apis
import spark_apis
import utils

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# import Meraki API info

from DEVNET_2593_init import MERAKI_API_KEY, MERAKI_URL
from DEVNET_2593_init import MERAKI_ORG, MERAKI_NETWORK, MERAKI_SM
from DEVNET_2593_init import MERAKI_CLIENT_MAC, MERAKI_PHONE_NO, MERAKI_GUEST_SSID, MERAKI_LOCATION

# import Spark API info

from DEVNET_2593_init import SPARK_TEAM, SPARK_ROOM, SPARK_EMAIL


def main():
    """
    The DEVNET_2593 app could run in two modes:
    - demo mode - printing output to console
    - debugging mode - printing and logging debug level messages to a file {DEVNET_2593.log}.
                     - errors will be logged to the file {DEVNET_2593_err.log}
    User input is required to select demo or debugging mode. If no user i
    """

    # save the initial stdout
    initial_sys = sys.stdout

    user_input = utils.get_input_timeout('If running in Debugging Mode please enter  y ', 10)
    user_input = 'n'
    # this section will determine if running the code in demo mode or logging debug to a file

    if user_input == 'y':
        # open a log file 'DEVNET_2593.log'
        file_log = open('DEVNET_2593.log', 'w')

        # open an error log file 'DEVNET_2593_err.log'
        err_log = open('DEVNET_2593_err.log', 'w')

        # redirect the stdout to file_log and err_log
        sys.stdout = file_log
        sys.stderr = err_log

        # configure basic logging to send to stdout, level DEBUG, include timestamps
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=('%(asctime)s - %(levelname)s - %(message)s'))

    # check if we have the Spark space created

    spark_room_id = None
    spark_room_id = spark_apis.get_room_id(SPARK_ROOM)
    if spark_room_id is None:
        spark_room_id = spark_apis.create_room_no_team(SPARK_ROOM)
        print('\nCreated the Spark Room with the name: ', SPARK_ROOM)
    else:
        print('\nFound Spark room with the name: ', SPARK_ROOM)

    # check where clients are, initial run of the code
    # check the location based on Wi-Fi association

    client_status = 'out'
    all_meraki_clients = meraki_apis.get_all_mac_clients(MERAKI_ORG, MERAKI_NETWORK, 300)

    print('\nAll Meraki Clients list ')
    utils.pprint(all_meraki_clients)

    if MERAKI_CLIENT_MAC in all_meraki_clients:
        print('\nClient in the office connected to Wi-Fi')
        client_status = 'in'
    else:
        print('\nClient not connected to Wi-Fi')
        client_status = 'out'

    # check location based on the GPS location from SM

    client_sm_status = 'out'

    client_location = meraki_apis.get_location_cell(MERAKI_ORG, MERAKI_SM, MERAKI_PHONE_NO)
    print('\nThe Meraki SM client with the ', MERAKI_PHONE_NO, ' location is: ', client_location)

    if client_location == MERAKI_LOCATION:
        print('\nClient in the office based on SM GPS location')
        client_sm_status = 'in'
    else:
        print('\nClient not in the office based on SM GPS location')
        client_sm_status = 'out'

    # define initial state of the Guest SSID based on client status

    if client_status == 'out':
        if client_sm_status == 'out':
            meraki_apis.disable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
            print('\nThe "MerakiConnect" SSID is disabled')
            ssid_status = 'off'
    else:
        meraki_apis.enable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
        print('\nThe "MerakiConnect" SSID is enabled')
        ssid_status = 'on'

    # infinite loop to check client status every minute

    while True:
        previous_ssid_status = str(ssid_status)

        # check the location based on Wi-Fi association

        all_meraki_clients = meraki_apis.get_all_mac_clients(MERAKI_ORG, MERAKI_NETWORK, 300)
        if MERAKI_CLIENT_MAC in all_meraki_clients:
            client_status = 'in'
        else:
            client_status = 'out'

        # check location based on the GPS location from SM

        client_location = meraki_apis.get_location_cell(MERAKI_ORG, MERAKI_SM, MERAKI_PHONE_NO)

        if client_location == MERAKI_LOCATION:
            client_sm_status = 'in'
        else:
            client_sm_status = 'out'

        if client_status == 'out':
            if client_sm_status == 'out':
                meraki_apis.disable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
                print('\nThe "MerakiConnect" SSID is disabled')
                ssid_status = 'off'
        else:
            meraki_apis.enable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
            print('\nThe "MerakiConnect" SSID is enabled')
            ssid_status = 'on'


        if ssid_status != previous_ssid_status:
            print('Status Change')
            if ssid_status == 'on':
                meraki_apis.enable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
                spark_apis.post_room_message(SPARK_ROOM, 'Welcome Dr. Z to your office. Have a great day!')
                spark_apis.post_room_message(SPARK_ROOM, 'The "MerakiConnect" SSID is enabled')
                print('\nWelcome! The "MerakiConnect" SSID is enabled')
            else:
                meraki_apis.disable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
                spark_apis.post_room_message(SPARK_ROOM, 'Good Bye Dr. Z! The "MerakiConnect" SSID is disabled')

        print('App is running normal, Guest SSID current status', ssid_status, ', Guest SSID previous status',
              previous_ssid_status)
        previous_ssid_status = ssid_status

        time.sleep(10)  # repeat every 10 seconds

    # restore the stdout to initial value
    sys.stdout = initial_sys

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
