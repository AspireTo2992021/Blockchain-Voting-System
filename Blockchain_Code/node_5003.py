
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import rsa 
from rsa.key import PrivateKey , PublicKey
# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        #self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
        f = open("store_chain.txt", "r")
        #note that file should not be empty, it should atleast contain []
        l=[]
        try :
         l = eval(f.read())
        except SyntaxError:
            print("file should not be empty, it should atleast contain []")
        except :
            print("something else went wrong")
        
        if len(l)==0:
                
                print("\n Creating Blockchain")
                self.create_block(proof = 1, previous_hash = '0')
                print(self.chain)
                
        else:
                print("******************\n \n \n")
                print("\n Appending Existing Blockchain\n")
                print(l)
                self.chain=l
                print("\n Chain: \n")
                print(self.chain)
       


    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    

    def last_balance(self,account_id,is_receiver)->int:
        
        #if account is present in list return that account balance
        # else return 1
        
        chain = self.chain
        #print("Chain[-1:]",chain[-1:0:-1])
        for block in chain[-1:0:-1]:
            transactions = block["transactions"]
            #print("Check Transactions , in transaction")
            print(transactions)
            for t in transactions:

                if(t["input"][0]["receiver"]==account_id):
                    return t["input"][0]["amount"]
                elif (t["input"][1]["sender"]==account_id):
                    return t["input"][1]["amount"]
                
        if(is_receiver):
            return 0
        else :
            return 1

    def make_double_entry_book(self,transactions):
        print("***********Transaction : ")
        print(transactions)
        #transaction[{}]
        """
        new_transaction[
            {
                "output":output_list[{"sender":t["sender"],"amount":t["amount"]}],
                "input" : input_list[{"receiver": t["receiver"],"amount":last_balance()+1},
                {"sender":t["sender"] , "amount": last_balance()-1}]
                
                }
                ]
        
        """
        main_list = list()
        #main_list=[[{"key" : {"name":"","amount":"" }}]]
        #new_transacton =[{"key" : {"name":"","amount":"" }}]
        output_list=list()
        input_list=list()
        new_transaction=[]
        for t in transactions:
            
            book_entry =dict()
            receiver_current_balance = self.last_balance(t["receiver"],True)
            sender_current_balance = self.last_balance(t["sender"],False)

            if(sender_current_balance < 1 ):
                continue
            #output 
            output_list.append({"sender":t["sender"] , "current_balance": sender_current_balance})

            #input
            
            input_list.append({"receiver": t["receiver"],"amount":receiver_current_balance+1})
            input_list.append({"sender":t["sender"] , "amount":sender_current_balance-1})

            #Transaction
            book_entry["output"]=output_list
            book_entry["input"] = input_list

            #appending transaction 
            new_transaction.append(book_entry)
            
        return new_transaction

    
    def create_block(self, proof, previous_hash):
        
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.make_double_entry_book(self.transactions)}
        self.transactions = []
        self.chain.append(block)
        self.storing_chain()
        
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
 
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            self.storing_chain()
            return True
        return False

    def storing_chain(self):
        print("Writing in File \n")
        print(str(self.chain))
        f = open("store_chain.txt", "w")
        f.write(str(self.chain))
        f.close()

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5001
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(sender = node_address, receiver = 'trial', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': ' The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():


  try:
    json = request.get_json()
    print(json)
    """ privatekey = PrivateKey(8928429708723078367968408861159334506063110426565729327112925060107811252957539657740519188800753824003801730358296590317594677676593972782731522508866801, 65537, 7980915653698145733743157726237638799978472237195379029264833237274147403585013383151331546783311427120008301328966463986393148773098771649605914910996385, 7374407942153548754663164198054381032220371048027587764755178234877068538757363637, 1210731733145170777170546913627385186032517448732030360185540371933504973)
    # process of parsing

    
    js=json.replace("\\\\",'\\' )
    #print("js:\n",js)
    js=js[7:len(js)-1-1]

    js=eval(js) #str(bytes) to bytes"""
    json = eval(json)
    json = eval(json["t"])
    json['sender'] = str(json['sender'])
    json['receiver'] = str(json['receiver'])
    print(f'json is {json}')
  except:
      print("Error in add_transaction")
      #print(js)
      return "500",500
  else:
    """    dm =  rsa.decrypt(js, privatekey)
    json = dm.decode()
    json=eval(json)"""
    #print("json1: ",json1)
    #print("type of json: ", type(json1))
    
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain



# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200
    
@app.route('/vote_count',methods=['GET'])
def balance():
    json = request.get_json()
    l = ["address"]
    if not all(key in json for key in l) :
        return 'Some elements of the request are missing', 400
    bal = blockchain.last_balance(json["address"],True)
    response = {"amount": bal}
    return jsonify(response),200

# Running the app
if __name__ == '__main__':
    app.debug = True
    app.run(port=5003)
#app.run(host = '0.0.0.0', port = 5001)
