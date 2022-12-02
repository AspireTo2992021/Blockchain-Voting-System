# scans QR code , if file exists procced with transaction else return authentication error
from utils import scan_QR_code,validate_QR_Code
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
from Crypto.PublicKey import RSA


key_file_path = "RequiredFiles/key.json"
download_file_path = "RequiredFiles/downloaded_file.txt"

app = Flask(__name__)



def user_autorisation_QR():
    name = scan_QR_code()
    file_name = 'text/'+name+'.txt'

    if(validate_QR_Code(file_name)):
        #redirect to voting page from where we will get the vote and receivers address
        print("QR validated")


    else : 
        print("User not validated")
        return "User not Valid"
#user_autorisation_QR
#text/pkey.txt
#file_name = "pkey"
#print('text/'+file_name+'.txt')

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
     try : 
        json = request.get_json()
        transaction_keys = ['receiver', 'amount']

        if not all(key in json for key in transaction_keys):
            return 'Some elements of the transaction are missing', 400
        f = open(download_file_path,'r')
        private_key = RSA.import_key(f.read())
        public_key=private_key.publickey().export_key()
        
     except Exception as e :
         print(f'Exception in method  add_transaction of frontend app.py {e} ')
         return False


