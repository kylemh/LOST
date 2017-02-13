# This program demonstrates how to encrypt a message

# Asymmetric Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Symmetric Crypto
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Other
import sys

def main():
    # Check the argument count
    if len(sys.argv) != 4:
        print("Usage: python3 %s <key file> <in file> <out file>"%sys.argv[0])
        return
    kf = sys.argv[1]
    df = sys.argv[2]
    of = sys.argv[3]

    # Make a symmetric key
    skey = get_random_bytes(16)
    cipher_aes = AES.new(skey, AES.MODE_EAX)
    
    # Read the asymmetric key -- Must be the recipient's public key
    with open(kf,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
        print(key.size_in_bytes())
        
    # Output the encrypted symmetric key, nonce, tag, and cipher text
    cipher_rsa = PKCS1_OAEP.new(key)
    with open(of,"wb") as outfile:
        skey_e = cipher_rsa.encrypt(skey)
        # The encrypted skey will be the length of the RSA key
        outfile.write(skey_e)
    
        # Read/encrypt the data
        with open(df,"rb") as datafile:
            data = datafile.read()
        cipher_text, tag = cipher_aes.encrypt_and_digest(data)
        print(len(cipher_text))
        # The cipher has a nonce and tag, each 16 bytes long
        # These will be needed to decrypt the message
        outfile.write(cipher_aes.nonce)
        outfile.write(tag)
        outfile.write(cipher_text)


if __name__=="__main__":
    main()
