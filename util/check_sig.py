# This program demonstrates how to verify a signature

# A signature is computed by:
#   1. Generating a cryptographic hash of the data to be signed
#   2. Encrypt the hash with the signer's private key
# A valid signature indicates that the data was not changed after the signature
# was generated and indicates who the sender likely is.

# To verify the signature, the verifier
#   1. Generates a cryptographic hash of the data in question
#   2. Decrypts the signature with the signer's public key
#   3. Verifies the computed hash matches the decrypted hash
# If the computed and decrypted hash do not match, the data was changed or the
# a different key was used for encryption.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pkcs1_15
import binascii

import sys

def main():
    # Check the arguments
    if len(sys.argv) != 4:
        print("Usage: python3 %s <key file> <data file> <signature>"%sys.argv[0])
        return
    kf = sys.argv[1]
    df = sys.argv[2]
    sig = binascii.unhexlify(sys.argv[3])

    # Compute the hash
    with open(df,"rb") as datafile:
        h = SHA3_256.new(datafile.read())
    # Check the signature
    with open(kf) as keyfile:
        # Read in the public key
        key = RSA.import_key(keyfile.read())
        try:
            # match the signature
            pkcs1_15.new(key).verify(h, sig)
            print("Signature verified")
        except (ValueError, TypeError):
            print("Verification failed")

if __name__=='__main__':
    main()
