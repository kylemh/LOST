This directory contains python clients to exercise web services

To use the encryption enabled service calls, ../util/osnap_crypto.py must be 
copied into this directory.

files:
p_activate_user.py - plaintext call for user activation
p_add_asset.py     - plaintext call for adding an asset
p_add_product.py   - plaintext call for adding a product
p_list_products.py - plaintext call for listing products
p_lost_key.py      - plaintext call for requesting the public key
p_suspend_user.py  - plaintext call for user deactivation

e_suspend_user.py  - encryption enabled call for user deactivation
