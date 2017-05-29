
# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


# !/usr/bin/env python3



import spark_apis
import meraki_apis
import utils
import logging
import sys

import json
import select
import requests
import time
import requests.packages.urllib3
import PIL
import os
import os.path


from PIL import Image, ImageDraw, ImageFont
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# import Meraki API info

from DEVNET_2593_init import MERAKI_URL, MERAKI_API_KEY, MERAKI_ORG, MERAKI_NETWORK

# import Spark API info

from DEVNET_2593_init import SPARK_URL, SPARK_AUTH, SPARK_MERAKI_ROOM



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






    # restore the stdout to initial value
    sys.stdout = initial_sys

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
