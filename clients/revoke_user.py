import sys
import json
import requests


arguments = {
    'username': str(sys.argv[2])
}

api_url = (str(sys.argv[1]) + "rest/revoke_user")
api_header = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
api_data = {'arguments': json.dumps(arguments)}

try:
    response = requests.post(url=api_url, headers=api_header, data=api_data)
    status = response.status_code
    print('HTTP Status:', status, ' - Please verify that the user\'s access has been revoked.')
except requests.exceptions.RequestException as err:
    print('HTTP Request Failed')
    print('Check to see if server is running or if domain is down.')
    print(err)
