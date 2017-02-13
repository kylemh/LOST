This directory contains some utilities to help interact with the LOST
application.

To run the osnap_crypto.py file to test functionality, you'll need to generate lost and hr keys. This can be done using osnap-keygen.py
python3 osnap-keygen.py lost
python3 osnap-keygen.py hr

Once the keys are generated, running osnap_crypto.py will execute some tests.
[osnapdev@osnap-image util]$ python3 osnap_crypto.py 
symmetric encrypt/decrypt working
signed encrypt/decrypt working

Files:
osnap-keygen.py - A program to generate key pairs
check_sig.py	- A program to check a datafile against a signature
sign.py		- A program to generate a signature for a datafile
encrypt.py	- A program to encrypt messages using RSA to protect an AES key
decrypt.py	- A program to decrypt messages using RSA to protect an AES key
plain_text_tool.py - A program to communicate with the webservice via plain text
api_stub.html	- A simple HTML form to allow plaintext to be submitted to the webservice
osnap_crypto.py - A library to handle the crypto component of HW5
