# This program can be used to generate a key pair for OSNAP systems

from Crypto.PublicKey import RSA
import sys

def main():
    # Check that the right number of args were provided
    if len(sys.argv) != 2:
        print("Usage: python3 %s <app name>"%sys.argv[0])
        return
    app = sys.argv[1]

    # Generate the key pair
    key = RSA.generate(2048)
    private_key = key.exportKey(pkcs=8)
    # Write out the private key
    with open("%s.priv"%app,'wb') as f:
        f.write(private_key)
    # Write out the public key
    with open("%s.pub"%app,'wb') as f:
        f.write(key.publickey().exportKey(format='OpenSSH'))

if __name__=="__main__":
    main()
