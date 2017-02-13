# This program demonstrates how to sign a message

# A signature is computed by:
#   1. Generating a cryptographic hash of the data to be signed
#   2. Encrypt the hash with the signer's private key
# A valid signature indicates that the data was not changed after the signature
# was generated and indicates who the sender likely is.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pkcs1_15
import binascii

import sys

def main():
    # Check the argument count
    if len(sys.argv) != 3:
        print("Usage: python3 %s <key file> <data file>"%sys.argv[0])
        return
    kf = sys.argv[1]
    df = sys.argv[2]

    # Generate the hash
    with open(df,"rb") as datafile:
        h = SHA3_256.new(datafile.read())
    # Generate the signature
    with open(kf) as keyfile:
        key = RSA.import_key(keyfile.read())
        sig = pkcs1_15.new(key).sign(h)
        # Encode signature as a hex string
        ashex = str(binascii.hexlify(sig),'ascii')
    # print the signature
    print(ashex)

if __name__=="__main__":
    main()
