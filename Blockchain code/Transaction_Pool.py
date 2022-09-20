
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import random 
import rsa 
from rsa.key import PrivateKey , PublicKey
 

def encrypt_transaction(obj):
    publickey = PublicKey(8928429708723078367968408861159334506063110426565729327112925060107811252957539657740519188800753824003801730358296590317594677676593972782731522508866801, 65537)
    mes = str(obj).encode()
    print(f"encoded text = {mes} ")
    em = rsa.encrypt(mes, publickey)
    return em 


# Creating a Web App
tp = Flask(__name__) # tp for transaction pool 


nodes = ["http://192.168.0.126:5001","http://192.168.0.126:5002","http://192.168.0.126:5003"]


class Connect_nodes :
    def __init__(self):
        # Connecting all nodes
        for node in nodes :
            l = []
            d = {}
            for connect_node in nodes :
                if connect_node is not node :
                    l.append(connect_node)
            d["nodes"]=l 
            r = requests.post(f"{node}/connect_node",json = d )
            print(f"reuslt of connection of {node}'th node ",r.json())

connection1 = Connect_nodes()

@tp.route('/add_transaction', methods = ['POST'])
def add_transactions():
    obj = request.get_json()
    

    print("obj: ",obj)
    transaction_keys = ['sender','receiver','amount']
    
    if not all(key in obj for key in transaction_keys):
        return 'keys inappropriate'
    
    """url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, json = myobj)

"""
#assign node randomly
    mine_node = random.choice(nodes)
    
    
    #valid node: directling applying largest chain to all nodes.
    # need to work here as corrupt node can create fake longest chain resulting in mess 
    
    """
    #need to use assymetric cyrptography  between transaction pool and nodes.
    #Assymetric cryptography between transaction pool and hadcoin)mode_5001.py is complete


    """
    #encypting transaction
    encoded_transaction = {}
    encoded_transaction["t"] = str(encrypt_transaction(obj))
    
    for node in nodes :
         requests.get(f"{node}/replace_chain")
    #mine block
    #requests.post(f"{mine_node}/add_transaction",json=obj)

    response=requests.post(f"http://192.168.0.126:5001/add_transaction",json=json.dumps(encoded_transaction)) 
    # problem is cannot send obj which is dictionary to json , which accepts JSON form
    #above proble, is solved
    
    print(response) 


    result = requests.get(f"http://192.168.0.126:5001/mine_block")
    #result = requests.get(f"{node}/mine_block")

    #Replace chain for all nodes
    for node in nodes :
         requests.get(f"{node}/replace_chain")
    print(f"result node : {mine_node}")
    print(f"result: {result.json()} typr : {type(result)} content type : {result.headers['Content-Type']}")
    return jsonify(result.json())

   
@tp.route('/check', methods = ['GET'])  
def check():
        return "working"
    





#Running transaction pool on 6000
tp.run(host = '0.0.0.0', port = 6000)