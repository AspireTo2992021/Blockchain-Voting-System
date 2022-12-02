from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json
import binascii
import base58
from utils import  calculate_hash
from validate import validate_signature
#from node.block import Block



def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        return pkcs1_15.new(public_key_object).verify(transaction_hash, signature)


def convert_transaction_data_to_bytes(transaction_data):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"]= str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["amount"] = str(transaction_data["amount"])
    return json.dumps(new_transaction_data,indent=2).encode('utf-8')


private_key = RSA.generate(1024)
print(f'private_key : {private_key}' )
public_key = private_key.publickey().export_key()
print(private_key)
print(public_key)

hash_1 = calculate_hash(public_key, hash_function="sha256")
hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
address = base58.b58encode(hash_2)

transaction_data = { "sender": address,"receiver" : b'blabliblou' , "amount" :1 }

print(address)

transaction_data = convert_transaction_data_to_bytes(transaction_data)
print("transactin in bytes")
print(f'{(type(transaction_data))}')
hash_object = SHA256.new(transaction_data)
signature = pkcs1_15.new(private_key).sign(hash_object)
#signature = binascii.hexlify(signature).decode("utf-8")

print(validate_signature(public_key , signature , transaction_data))

