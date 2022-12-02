from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import json
#sign the transaction
private_key = RSA.generate(1024)

public_key = private_key.publickey().export_key()
print(private_key)
print(public_key)

user_dict = {'name': 'dinesh', 'code': 'dr-01'}
user_encode_data = json.dumps(user_dict, indent=2).encode('utf-8')

message = user_encode_data
key = RSA.import_key(private_key.export_key())
h = SHA256.new(message)
signature = pkcs1_15.new(key).sign(h)

#check the signed transaction
key = RSA.import_key((public_key))
h = SHA256.new(message)
try:
    pkcs1_15.new(key).verify(h, signature)
    print ("The signature is valid.")
except (ValueError, TypeError):
   print ("The signature is not valid.")