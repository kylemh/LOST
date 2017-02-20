# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime
from osnap_crypto import decrypt, encrypt_and_sign

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<3 :
        print("Usage: python3 %s <hr.priv> <lost.pub> <url> <username>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['timestamp'] = datetime.datetime.utcnow().isoformat()
    args['username']  = sys.argv[4]

    # Print a message to let the user know what is being tried
    print("Suspending user: %s"%args['username'])

    # Setup the data to send
    (data, sig, skey, nonce) = encrypt_and_sign(json.dumps(args), sys.argv[2], sys.argv[1])
    sargs = dict()
    sargs['arguments']=data
    sargs['signature']=sig
    data = urlencode(sargs)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    req = Request(sys.argv[3],data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Parse the response
    data = decrypt(res.read(), skey, nonce)
    resp = json.loads(data)
    
    # Print the result code
    print("Call to LOST returned: %s"%resp['result'])
    

if __name__=='__main__':
    main()
