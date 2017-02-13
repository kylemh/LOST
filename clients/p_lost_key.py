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
    if len(sys.argv)<2 :
        print("Usage: python3 %s <url>"%sys.argv[0])
        return
    
    # Print a message to let the user know what is being tried
    print("Requesting the LOST public key")

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=''
    sargs['signature']=''
    data = urlencode(sargs)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    req = Request(sys.argv[1],data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Parse the response
    resp = json.loads(res.read().decode('ascii'))
    
    # Print the result code
    print("Call to LOST returned: %s"%resp['result'])
    print("Key returned in base64:\n%s"%resp['key'])
    

if __name__=='__main__':
    main()
    
