# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


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
from DEVNET_2593_init import MERAKI_ORG, MERAKI_NETWORK
from DEVNET_2593_init import MERAKI_CLIENT_MAC, MERAKI_PHONE_NO, MERAKI_GUEST_SSID

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

    # check where clients are

    client_status = 'out'
    all_meraki_clients = meraki_apis.get_all_mac_clients(MERAKI_ORG, MERAKI_NETWORK, 600)

    print('\nAll Meraki Clients list ')
    utils.pprint(all_meraki_clients)

    if MERAKI_CLIENT_MAC in all_meraki_clients:
        print('\nClient in the office connected to Wifi')
        client_status = 'in'

    client_location = meraki_apis.get_location_cell(MERAKI_ORG, MERAKI_NETWORK, MERAKI_PHONE_NO)
    print('\nThe Meraki SM client with the ', MERAKI_PHONE_NO, ' location is: ', client_location)

    if client_location == '23742 SW Pinehurst Dr, Sherwood, OR 97140, USA':
        print('\nClient in the office based on SM GPS location')
        client_status = 'in'

    if client_status == 'in':
        meraki_apis.enable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
        print('\nThe "MerakiConnect" SSID is enabled')
    else:
        meraki_apis.disable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
        print('\nThe "MerakiConnect" SSID is disabled')

    # check if we have the Spark team created
    spark_team_id = None
    spark_team_id = spark_apis.get_team_id(SPARK_TEAM)
    if spark_team_id is None:
        spark_team_id = spark_apis.create_team(SPARK_TEAM)
        print('\nCreated the Spark Team with the name: ', SPARK_TEAM)
    spark_apis.add_team_membership(SPARK_TEAM, SPARK_EMAIL)
    print('\nAdded membership to the team ', SPARK_TEAM)

    # check if we have the Spark space created
    spark_room_id = None
    spark_room_id = spark_apis.get_room_id(SPARK_ROOM)
    if spark_room_id is None:
        spark_room_id = spark_apis.create_room(SPARK_ROOM, SPARK_TEAM)
        print('\nCreated the Spark Space with the name: ', SPARK_ROOM)

    # infinite loop to check client status every minute

    while True:
        new_client_status = 'out'
        all_meraki_clients = meraki_apis.get_all_mac_clients(MERAKI_ORG, MERAKI_NETWORK, 60)
        if MERAKI_CLIENT_MAC in all_meraki_clients:
            new_client_status = 'in'
        client_location = meraki_apis.get_location_cell(MERAKI_ORG, MERAKI_NETWORK, MERAKI_PHONE_NO)
        if client_location == '23742 SW Pinehurst Dr, Sherwood, OR 97140, USA':
            new_client_status = 'in'

        if new_client_status != client_status:
            print('Status Change')
            if new_client_status == 'in':
                meraki_apis.enable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
                spark_apis.post_room_message(SPARK_ROOM, 'Welcome Gabi! The "MerakiConnect" SSID is enabled')
                print('\nWelcome! The "MerakiConnect" SSID is enabled')
            else:
                meraki_apis.disable_ssid(MERAKI_ORG, MERAKI_NETWORK, MERAKI_GUEST_SSID)
                spark_apis.post_room_message(SPARK_ROOM, 'Good Bye Gabi! The "MerakiConnect" SSID is disabled')
        print('App is running normal, client current status', new_client_status, ', client previous status',
              client_status)
        client_status = new_client_status
        time.sleep(60)

    # restore the stdout to initial value
    sys.stdout = initial_sys

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
