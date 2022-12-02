import datetime
import hashlib
import json
from flask import Flask, jsonify, request , render_template , redirect , url_for
import requests
from uuid import uuid4
from urllib.parse import urlparse
from wallet import validate_signature 
from wallet import Transaction
from wallet import initialize_wallet
from utils import scan_QR_code,validate_QR_Code ,convert_transaction_data_to_bytes
from validate import change_dictionary_keys

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import os
from flask_dropzone import Dropzone
from forms import QRCodeData
import secrets
import cv2
import qrcode


#Assumption : front end will use /make_transaction to send transaction 
""""
{
'receiver_address' = '',
'amount'=''
}

"""
#Assumption: private key right now is static, after integration with frontend , private key will be taken from QR code.
#therefore methods should be changed accordingly

key_file_path = "../RequiredFiles/key.json"
download_file_path = "../RequiredFiles/downloaded_file.txt"

app = Flask(__name__)
print(app.config)


dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['SECRET_KEY'] = 'bf9b1b2111ab03c26782b1e7da3fd366fc5e127b'

app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'user_authorisation_QR'

dropzone = Dropzone(app)


#app.config["SERVER_NAME"] = 'localhost:3000'

#take transaction input 
# sign it
#send it to pool


decoded_info = ""

@app.route("/")
def home():
    return render_template('layout.html')


@app.route("/decqr", methods=["GET", "POST"])
def decqr():
    if request.method == 'POST':
        global decoded_info
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".png"
       

        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
        f.save(file_location)

        print(file_location)
        # read and decode QRCode
        img = cv2.imread(file_location)

        det=cv2.QRCodeDetector()

        val, pts, st_code=det.detectAndDecode(img)
        print(f"data from qr {val}")
        
        os.remove(file_location)
        decoded_info = val
        redirect(url_for('user_authorisation_QR'))
        print("redirect failed")
        return render_template("layout.html")
        
    else:
       return render_template("upload.html")

@app.route("/decoded")
def decoded():
    global decoded_info
    redirect(url_for('user_authorisation_QR'))
    return render_template("decoded.html", data=decoded_info)

@app.route("/user_authorisation_QR")
def user_authorisation_QR():
    #name = scan_QR_code()
    name = decoded_info
    file_name = 'text/'+name+'.txt'

    if(validate_QR_Code(file_name)):
        #redirect to voting page from where we will get the vote and receivers address
        #redirect to voteing or ig make transaction
        print("QR validated")
        return render_template("vote.html")

    else : 
        print("User not validated")
        return render_template("not_eligible.html")
    return "User not Valid"
#user_autorisation_QR()



@app.route("/vote")
def vote():
    return render_template("vote.html")

@app.route("/not_eligible")
def not_eligible():
    return render_template("not_eligible.html")


def send_to_pool(transaction):
 while(1):  

    try :
        response=requests.post(f"http://127.0.0.1:5000/add_transaction",json=json.dumps(transaction)) 
        return response
    except Exception as e :
        print(e)

      

@app.route('/make_transaction',methods=['POST'])
def transaction():
    json = request.get_json()
    transaction_keys = [ 'receiver_address', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    try: 
        f = open(download_file_path,'r')
        private_key = RSA.import_key(f.read())
        
        owner = initialize_wallet(private_key)    
        T = Transaction(owner ,receiver_address = json["receiver_address"],amount = json["amount"])
        T.sign()
        #sending to transaction pool
        resp = send_to_pool(T.send_to_nodes(owner.public_key)) #for now we need to send public key as it will be checking signing details
   
    except Exception as e :
       print(f'Error from Wallet IN method in transaction ')
       return "Failed to Vote" , 400
    
    #returning result back to front end
    return jsonify(resp)


@app.route('/test_make_transaction',methods=['POST'])
def test_transaction():
    
    if request.method == 'POST':
        if request.form.get('action1') == 'id1':
            json = {"receiver_address" : "candidate 1" ,"amount":1}
        elif  request.form.get('action2') == 'id2':
            json = {"receiver_address" : "candidate 2" ,"amount":1}
        else:
           json = {"receiver_address" : "candidate 3" ,"amount":1}
   

    print(json)
    ##########################################
    #json = request.get_json()
    #json = {"receiver_address " : "avs" ,"amount":1}
    transaction_keys = [ "receiver_address", "amount"]
    if not all(key in json for key in transaction_keys):
       return f'From test_make_transaction Some elements of the transaction are missing ', 400
    
    f = open(download_file_path,'r')
    private_key = RSA.import_key(f.read())
    public_key = private_key.publickey().export_key()

    owner = initialize_wallet(private_key)    
    T = Transaction(owner ,receiver_address = json["receiver_address"],amount = json["amount"])
    T.sign()
        #sending to transaction pool
        #resp = send_to_pool(T.send_to_nodes())
        #print(f'publick key {owner.public_key}')
    resp = T.send_to_nodes(owner.public_key)
    try:   
        r=send_to_pool(resp)
   

        print(f'response from pool {r.headers["Content-Type"]}')
        #resp = eval(resp["data"])
        print(f'output from transaction pool: {r.json()}')   
        #Transaction_data = change_dictionary_keys(resp["TransactionData"])

      
        #print(validate_signature(resp["public_key"] ,  resp["signature"] , convert_transaction_data_to_bytes(resp["TransactionData"])))
        #print(f'resp ')
        #print(f' public_key : {resp["public_key"]} , signature : {resp["signature"] } transaction_in_bytes : {convert_transaction_data_to_bytes(Transaction_data)}')
        #print(convert_transaction_data_to_bytes(Transaction_data))
        #f'{validate_signature(resp["public_key"] ,  resp["signature"], convert_transaction_data_to_bytes(Transaction_data))}'
        return r.json() , 200
    except Exception as e :
       print(f'Error from Wallet IN method test_make_transaction{e} ')
       response = {"message" : "something went wrong try again" , "code" : 400}
       return jsonify(response), 400
    
    #returning result back to front end
    #return jsonify(resp)
"""def send_to_pool_test(transaction ,  public_key):
    validate_signature(public_key,transaction.signature ,)
"""


app.debug = True
app.run('0.0.0.0',3000)







