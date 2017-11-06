

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
from DEVNET_2593_init import MERAKI_ORG, MERAKI_NETWORK
from DEVNET_2593_init import MERAKI_CLIENT_MAC, MERAKI_PHONE_NO, MERAKI_GUEST_SSID


def main():
    """
    This sample code will print info about:
    - The Meraki Organizations this user account has access to
    - The Meraki Networks associated with the organization
    - The Meraki Network Devices for the network
    - All the Meraki Clients for the network
    """

    # get the Meraki organizations

    meraki_orgs = meraki_apis.get_organizations()
    print('\nThe Meraki Organizations this user account has access to: \n')
    utils.pprint(meraki_orgs)

    # get the Meraki networks for the organization with the name "MERAKI_ORG"

    meraki_networks = meraki_apis.get_networks(MERAKI_ORG)
    print('\nThe Meraki Networks associated with the organization with the name', MERAKI_ORG, ':\n')
    utils.pprint(meraki_networks)

    # get the Meraki Network Devices for the network with the info: "MERAKI_ORG", "MERAKI_NETWORK"

    meraki_network_devices = meraki_apis.get_network_devices(MERAKI_ORG, MERAKI_NETWORK)
    print('\nThe Meraki Network Devices for the network with the name ', MERAKI_NETWORK, ':\n')
    utils.pprint(meraki_network_devices)

    # get all the Meraki Clients for the network with the info: "MERAKI_ORG", "MERAKI_NETWORK", connected during the
    # past timespan value entered by user

    timespan = input('Time Period for which you want to get all clients MAC addresses ? '
                     '(in seconds, less than 30 days, please enter an integer < 360000)  ')
    meraki_clients = meraki_apis.get_all_mac_clients(MERAKI_ORG, MERAKI_NETWORK, timespan)
    utils.pprint(meraki_clients)

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
