# OSNAP cryptographic routines

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pkcs1_15

# Asymmetric Crypto
from Crypto.Cipher import PKCS1_OAEP

# Symmetric Crypto
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import base64

def _gen_sig(key, message):
    h = SHA3_256.new(message)
    sig = pkcs1_15.new(key).sign(h)
    return base64.b64encode(sig)

def _check_sig(key, message, sig):
    h = SHA3_256.new(message)
    sig = base64.b64decode(sig)
    try:
        pkcs1_15.new(key).verify(h, sig)
    except (ValueError, TypeError):
        raise OSNAPSecurityException("Signature did not verify")
    return True

class OSNAPSecurityException(Exception):
    pass
    
def encrypt_and_sign(plaintext, recipient_pub, sender_priv):
    """Given a message and paths to keys, generate the ciphertext and signature"""
    
    # Make a symmetric key
    skey = get_random_bytes(16)
    cipher_aes = AES.new(skey, AES.MODE_EAX)
    
    # Read the asymmetric key -- Must be the recipient's public key
    with open(recipient_pub,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
    cipher_rsa = PKCS1_OAEP.new(key)
    
    # encrypt the symmetric key
    skey_e = cipher_rsa.encrypt(skey)
    # encrypt the message
    cipher_text, tag = cipher_aes.encrypt_and_digest(plaintext.encode('utf-8'))
    data = b''.join([skey_e, cipher_aes.nonce, tag, cipher_text])
    
    # Read the asymmetric key -- Must be the sender's private key
    with open(sender_priv,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
    sig  = _gen_sig(key, data)
    
    return (base64.b64encode(data), sig, skey, cipher_aes.nonce)

def decrypt_and_verify(ciphertext, sig, recipient_priv, sender_pub):
    """Given a message and path to a key, recover the plaintext
    
    returns the message and nonce
    Throws OSNAPSecurityException
    """
    # Convert the ciphertext back to binary data
    raw = base64.b64decode(ciphertext)
    # Check the signature
    with open(sender_pub,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
    _check_sig(key, raw, sig)
    
    # Read the asymetric key -- Must be the recipient's private key
    with open(recipient_priv,"rb") as keyfile:
        key = RSA.import_key(keyfile.read())
        cipher_rsa = PKCS1_OAEP.new(key)
    
    # Take apart the message
    eskey = raw[:key.size_in_bytes()] # encrypted symmetric key
    offset = key.size_in_bytes()
    nonce = raw[offset:offset+16] # nonce
    offset += 16
    tag   = raw[offset:offset+16] # tag
    offset += 16
    cipher_text = raw[offset:] # encrypted data
    
    # Recover the symmetric key
    skey = cipher_rsa.decrypt(eskey)
    
    # Make the AES cipher.
    cipher_aes = AES.new(skey, AES.MODE_EAX, nonce)
    
    # Do the decryption and check the authenticity
    data = cipher_aes.decrypt_and_verify(cipher_text, tag)
    
    return (data.decode("utf-8"), skey, nonce)
    
def encrypt(plaintext, skey, nonce):
    """Given a known nonce and secret key, encrypt for a recipient"""
    cipher_aes = AES.new(skey, AES.MODE_EAX, nonce)
    ciphertext = cipher_aes.encrypt(plaintext.encode('utf-8'))
    return base64.encodebytes(ciphertext)


def decrypt(ciphertext, skey, nonce):
    """Given a known nonce and tag, decrypt a message"""
    cipher_aes = AES.new(skey, AES.MODE_EAX, nonce)
    plaintext = cipher_aes.decrypt(base64.decodebytes(ciphertext))
    return plaintext.decode("utf-8")

def main():
    skey = get_random_bytes(16)
    nonce = get_random_bytes(16)
    c = encrypt("hi",skey,nonce)
    p = decrypt(c,skey,nonce)
    if p=="hi":
        print("symmetric encrypt/decrypt working")
    
    (data, sig) = encrypt_and_sign('test message', 'lost.pub', 'hr.priv')
    (data, skey, nonce) = decrypt_and_verify(data, sig, 'lost.priv', 'hr.pub')
    if data=='test message':
        print("signed encrypt/decrypt working")

if __name__=="__main__":
    main()
