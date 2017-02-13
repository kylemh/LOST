# This program demonstrates how to decrypt a file

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

    # Read the asymetric key -- Must be the recipient's private key
    with open(kf,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
        cipher_rsa = PKCS1_OAEP.new(key)
    
    # Read the raw encrypted data
    with open(df,"rb") as datafile:
        eskey = datafile.read(key.size_in_bytes()) # encrypted symmetric key
        print(key.size_in_bytes())
        nonce = datafile.read(16) # nonce
        tag   = datafile.read(16) # tag
        cipher_text = datafile.read() # encrypted data
        print(len(cipher_text))
        
    # Recover the symmetric key
    skey = cipher_rsa.decrypt(eskey)
    
    # Make the AES cipher.
    cipher_aes = AES.new(skey, AES.MODE_EAX, nonce)
    
    # Do the decryption and check the authenticity
    data = cipher_aes.decrypt_and_verify(cipher_text, tag)
    
    # Spool to disk
    with open(of,"wb") as outfile:
        outfile.write(data)

if __name__=="__main__":
    main()
