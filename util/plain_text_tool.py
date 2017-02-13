# This client can be used to interact with the LOST interface prior to encryption
# implementation

import json
import sys

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<3 :
        print("Usage: python3 %s <url> <arg file>"%sys.argv[0])
        return
    
    # Setup the data to send
    args = dict()
    with open(sys.argv[2]) as f:
        args['arguments']=f.read()
    args['signature']=''
    data = urlencode(args).encode('ascii')
    
    # Make the resquest
    req = Request(sys.argv[1],data,method='POST')
    res = urlopen(req)
    
    # Spool the results to the user
    dat = res.read().decode("utf-8")
    print(dat)
    resp = json.loads(dat)
    print(resp)

if __name__=='__main__':
    main()
    
