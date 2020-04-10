# DEVNET_2593

Repo for Cisco Live US Presentation DEVNET-2593

This repository will be used for the Cisco Live US DEVNET-2593 session

**Software included:**

 - Spark_APIs_2593.py
 - Meraki_APIs_2593.py
 - SM_APIs_2593.py
 - DEVNET_2593.py full lab code
 
Three Python modules are included and required:

 - meraki_apis.py - Meraki functions
 - spark_apis.py - Spark functions
 - utils.py - some other useful functions
 
The file DEVNET_2593_init.py will have to be changed to match your Meraki Sandbox or lab environment.

During this lab we will use Cisco Spark and a Meraki DevNet Sandbox.

The DEVNET_2593 app could run in two modes:
    - demo mode - printing output to console
    - logging mode - printing and logging debug level messages to a file {DEVNET_2593.log}.
                     - errors will be logged to the file {DEVNET_2593_err.log}
    User input is required to select demo or logging mode. If no user input in will run in demo mode

**Application Workflow:**

- Check if existing Spark room, and create a new room if not
- It will identify if pre-defined Doctor cellphone are connected to the corporate Wi-Fi Meraki network
- It will collect the GPS coordinate of the Doctor cellphone using the Meraki Systems Manager APIs
- When Doctor presence is determined to be in the office, enable the Guest SSID
- Post message to welcome Doctor to the office
- When Doctor leaves the office, cellphone disconnecting from the Corporate Wi-Fi and GSP coordinates not matching the office address disable the Guest SSID.
- Post a message in the Spark room and close the room

This Application is intended as a demo and collects information from one mobile device for one location