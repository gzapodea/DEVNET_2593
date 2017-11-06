
# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

# !/usr/bin/env python3

# A Cisco Meraki Network is required for this demo
# Attendees will need to register to use the DevNet Meraki Sandbox if no other options
# The Meraki Dashboard API Key will be copied from the Meraki dashboard > user > profile
# according the presentation documentation

import logging
import sys


import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import meraki_apis
import utils

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# import Meraki API info

from DEVNET_2593_init import MERAKI_API_KEY, MERAKI_URL
from DEVNET_2593_init import MERAKI_ORG, MERAKI_NETWORK, MERAKI_SM
from DEVNET_2593_init import MERAKI_CLIENT_MAC, MERAKI_PHONE_NO, MERAKI_GUEST_SSID


def main():
    """
    This sample code will print info about:
    - The Meraki Organizations this user account has access to
    - The Meraki Networks associated with the organization
    - The Meraki Network Devices for the network
    - The GPS location for a mobile client, obtained from Meraki SM
    """

    # get the Meraki organizations

    meraki_orgs = meraki_apis.get_organizations()
    print('\nThe Meraki Organizations this user account has access to: \n')
    utils.pprint(meraki_orgs)

    # get the Meraki networks for the organization with the name "MERAKI_ORG"

    meraki_networks = meraki_apis.get_networks(MERAKI_ORG)
    print('\nThe Meraki Networks associated with the organization with the name', MERAKI_ORG, ':\n')
    utils.pprint(meraki_networks)

    # get the Meraki SM Clients for the network with the info: "MERAKI_ORG", "MERAKI_NETWORK"

    meraki_client_devices = meraki_apis.get_sm_devices(MERAKI_ORG, MERAKI_SM)
    print('\nThe Meraki SM Client Devices for the network with the name ', MERAKI_SM, ':\n')
    utils.pprint(meraki_client_devices)

    # get the location information for a SM client matching a user input phone number

    # phone = input('Please input a client phone number to locate using the SM location info for '
    #                     '(format 10 digits, no dashes nor spaces) : ')
    phone_number = '+1' + '5038904949'
    phone_location = meraki_apis.get_location_cell(MERAKI_ORG, MERAKI_SM, phone_number)
    if not phone_location:
        print('\nThe client with the cell phone number ', phone_number, ' may not be located at this time')
    else:
        print('\nThe client with the cell phone number ', phone_number, ' last known location is : ', phone_location)


    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
