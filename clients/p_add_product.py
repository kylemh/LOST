# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<6 :
        print("Usage: python3 %s <url> <vendor> <description> <alt_desc> <compartments>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['timestamp'] = datetime.datetime.utcnow().isoformat()
    
    prod = dict()
    prod['vendor']  = sys.argv[2]
    prod['description'] = sys.argv[3]
    prod['alt_description'] = sys.argv[4]
    prod['compartments'] = sys.argv[5]
    prod_list = list()
    prod_list.append(prod)
    args['new_products'] = prod_list

    # Print a message to let the user know what is being tried
    print("Add an item: %s"%prod)

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=json.dumps(args)
    sargs['signature']=''
    data = urlencode(sargs)
    
    # Make the resquest
    req = Request(sys.argv[1],data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Parse the response
    resp = json.loads(res.read().decode('ascii'))
    
    # Print the result code
    print("Call to LOST returned: %s"%resp['result'])
    

if __name__=='__main__':
    main()
    
