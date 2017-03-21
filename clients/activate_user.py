import json
import requests
import sys

if not (len(sys.argv) == 5):
    print("ERROR: Unsported Number of Arguments")
    print("USAGE: activate_user.py <host> <username> <password> <role>\n")
    print("NOTE: You may only use 'facofc' or 'logofc' for the user's role.\n")
    quit()

args = {
    'username': sys.argv[2],
    'password': sys.argv[3],
    'role': sys.argv[4]
}

