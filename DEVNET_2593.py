
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



def main():
    """
    The test module run in two modes:
    - demo mode - printing output to console
    - debugging mode - printing and logging debug level messages to a file python_modules.log.
    User input is required to select demo or debugging mode
    """

    # save the initial stdout
    initial_sys = sys.stdout

    user_input = utils.get_input_timeout('If running in Debugging Mode please enter  y ', 5)

    # this section will determine if running the code in demo mode or logging debug to a file

    if user_input == 'y':

        # open a log file 'python_modules.log'
        file_log = open('python_modules.log', 'w')

        # open an error log file 'python_modules_err.log'
        err_log = open('python_modules_err.log', 'w')

        # redirect the stdout to file_log and err_log
        sys.stdout = file_log
        sys.stderr = err_log

        # configure basic logging to send to stdout, level DEBUG, include timestamps
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=('%(asctime)s - %(levelname)s - %(message)s'))

