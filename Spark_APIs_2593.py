# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

# Spark Accounts are required for this demo
# Attendees will need to register to ciscospark.com if they do not have an account already
# The Spark token will be copied from developers.ciscospark.com


import requests
import json
import requests.packages.urllib3
import spark_apis

from requests.packages.urllib3.exceptions import InsecureRequestWarning

from DEVNET_2593_init import SPARK_URL, SPARK_AUTH, SPARK_ROOM, SPARK_TEAM, SPARK_EMAIL # the file includes all config data required for the lab

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def main():
    """
    Spark Accounts are required for this demo.
    Attendees will need to register to ciscospark.com if they do not have an account already.
    This lab module will ask users to create a team, a space, invite a new member to the space.
    The code will retrieve the space Spark Id and post a message to the space.
    Only some functions will be used. The other functions are provided as a reference.
    Few Python modules will be required:
    - utils.py
    - spark_apis.py
    - DEVNET_2593_init.py
    """

    # create a new Spark Team?

    print('\nSpark Team to be created with the name : ', SPARK_TEAM, '\n')

    new_team = input('Do you want to create a new Spark Team ? (y/n): ').upper()
    if new_team == 'Y':
        spark_apis.create_team(SPARK_TEAM)

    # check if we have the Spark team created
    spark_team_id = None
    spark_team_id = spark_apis.get_team_id(SPARK_TEAM)
    if spark_team_id is None:
        spark_team_id = spark_apis.create_team(SPARK_TEAM)
        print('\nCreated the Spark Team with the name: ', SPARK_TEAM)
    spark_apis.add_team_membership(SPARK_TEAM, SPARK_EMAIL)
    print('\nAdded membership to the team ', SPARK_TEAM)

    # create a new Spark Room?

    print('\nSpark Room to be created with the name : ', SPARK_ROOM, '\n')

    new_room = input('Do you want to create a new Spark Room ? (y/n): ').upper()
    if new_room == 'Y':
        spark_apis.create_room(SPARK_ROOM, SPARK_TEAM)

    # check if we have the Spark space created
    spark_room_id = None
    spark_room_id = spark_apis.get_room_id(SPARK_ROOM)
    if spark_room_id is None:
        spark_room_id = spark_apis.create_room(SPARK_ROOM, SPARK_TEAM)
        print('\nCreated the Spark Space with the name: ', SPARK_ROOM)

    # find the Spark room id for the room with the name 'SPARK_ROOM'

    devnet_room_id = spark_apis.get_room_id(SPARK_ROOM)
    print('\nThe Spark room id for the room with the name ', SPARK_ROOM, ' is: ', devnet_room_id, '\n')

    # ask the user to invite somebody to the Spark room

    membership_email = input('Enter an email address to invite user to your Spark room : ')
    spark_apis.add_room_membership(SPARK_ROOM, membership_email)

    # ask user to input a message to be posted in the room

    spark_message = input('Please input a message in the room : ')
    print('\nThis message will be posted in the room with the name ', SPARK_ROOM, ' : ', spark_message)

    # post a message in the room

    spark_apis.post_room_message(SPARK_ROOM, spark_message)

    print('\n\nEnd of Application Run \n')


if __name__ == '__main__':
    main()
