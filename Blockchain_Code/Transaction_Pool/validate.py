from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json
import requests
#from node.block import Block



def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        return pkcs1_15.new(public_key_object).verify(transaction_hash, signature)

def change_dictionary_keys(resp2):
        Transaction_data = dict()
        #resp2=eval(resp2)
        Transaction_data["sender"] = resp2["sender_address"]
        Transaction_data["receiver"] = resp2["receiver_address"]
        Transaction_data["amount"] = resp2["amount"]
        return {
        "sender": resp2["sender_address"],
        "receiver": resp2["receiver_address"],
        "amount" :  resp2["amount"]
    }

def convert_transaction_data_to_bytes(transaction_data):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"]= str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["amount"] = str(transaction_data["amount"])
    return json.dumps(new_transaction_data,indent=2).encode('utf-8')


def last_balance(account_id,node = "http://127.0.0.1:5003/")->int:
        
        #if account is present in list return that account balance
        # else return 1
    while(1): 
        print(f'acoount id  : {account_id}')
        response= requests.get(f"http://127.0.0.1:5003/get_chain")
        response = response.json()
        chain = response["chain"]
        #print("Chain[-1:]",chain[-1:0:-1])
        for block in chain[-1:0:-1]:
            transactions = block["transactions"]
            #print("Check Transactions , in transaction")
            
            for t in transactions:

                if(t["input"][0]["receiver"]==str(account_id)):
                    return t["input"][0]["amount"]
                elif (t["input"][1]["sender"]==str(account_id)):
                    return t["input"][1]["amount"]
                
        
        return 1



def validate_vote(transaction : dict):
    return last_balance(account_id=transaction["sender"])
        

"""transaction = {
    "sender" : "w1",
    "receiver" : "b1",
     "amount" : 1
}

print(f' fund validation output : {validate_funds(transaction)}')
"""



""" 
class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.signature = ""

    @staticmethod
    def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature)

    def validate_funds(self, sender_address: bytes, amount: int) -> bool:
        sender_balance = 0
        current_block = self.blockchain
        while current_block:
            if current_block.transaction_data["sender"] == sender_address:
                sender_balance = sender_balance - current_block.transaction_data["amount"]
            if current_block.transaction_data["receiver"] == sender_address:
                sender_balance = sender_balance + current_block.transaction_data["amount"]
            current_block = current_block.previous_block
        if amount <= sender_balance:
            return True
        else:
            return False
"""