import sys
import json
import requests


if not (len(sys.argv) == 5):
    print("ERROR: Unsupported Number of Arguments")
    print("USAGE: activate_user.py <host> <username> <password> <role>\n")
    print("NOTE: You may only use 'facofc' or 'logofc' for the user's role.\n")
    quit()

arguments = {
    'username': str(sys.argv[2]),
    'password': str(sys.argv[3]),
    'role': str(sys.argv[4])
}

api_url = (str(sys.argv[1]) + "rest/activate_user")
api_header = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
api_data = {'arguments': json.dumps(arguments)}

try:
    response = requests.post(url=api_url, headers=api_header, data=api_data)
    status = response.status_code
    print('HTTP Status:', status, ' - Please verify that the user has been added to the database.')
except requests.exceptions.RequestException as err:
    print('HTTP Request Failed')
    print('Check to see if server is running or if domain is down.')
    print(err)
