import json

from Crypto.Hash import RIPEMD160, SHA256
from urllib.parse import urlparse

import qrcode
import cv2
from Crypto.PublicKey import RSA


import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.cloud import storage
from google.oauth2 import service_account


#Assumption: private key right now is static, after integration with frontend , private key will be taken from QR code.
#therefore methods should be changed accordingly => method changed in wallet intialise_wallet(private_key)

""" Firebase connectivity """
#in system file path
# NOTE: in terminal use: run util.py to run file otherwise tempcode runner will eat ur mind
key_file_path = "../RequiredFiles/key.json" 
download_file_path = "../RequiredFiles/downloaded_file.txt"
#Connecting to bucket
cred = credentials.Certificate(key_file_path)
initialize_app(cred, {'storageBucket': 'project1-40e50.appspot.com'})


#QR CODE UTIL
#only scans from system, need to write for scanner 
def scan_QR_code():
    img=cv2.imread("medium.png")
    det=cv2.QRCodeDetector()
    val, pts, st_code=det.detectAndDecode(img)
    print(val)
    return val

def make_QR_code(name):
    qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
    qr.add_data(name)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="aqua")
    img.save(name+".png")

def validate_QR_Code(file_path_in_cloud) : 
    #scan qr and check if file exists in cloud , if exists qr validated else not validated

    credentials = service_account.Credentials.from_service_account_file(key_file_path)
    try :
         storage.Client(credentials=credentials).bucket(firebase_admin.storage.bucket().name).blob(file_path_in_cloud).download_to_filename(download_file_path)
         f = open(download_file_path,'r')
         key = RSA.import_key(f.read())
         pkey=key.publickey().export_key()

         print(pkey)
         return True
    except Exception as e:
         print(f'exception from method validate_QR_Code: {e}') 
         return False
#text/pkey.txt is file path in cloud of project1    
#validate_QR_Code("text/pkey.txt")

make_QR_code("voter4")

""" Encryption Utils   """
def calculate_hash(data, hash_function="sha256"):
    if(type(data)==str):
        data = bytearray(data,"utf-8")

    if hash_function == "sha256" :
        h= SHA256.new()
        h.update(data)
        return h.hexdigest() 
    if hash_function == "ripemd160":
        h=RIPEMD160.new()
        h.update(data)
        return h.hexdigest()




def generate_transaction_data(sender_bitcoin_address , receiver_bitcoin_address,amount)->dict:
    return {
        "sender": sender_bitcoin_address,
        "receiver": receiver_bitcoin_address,
        "amount" : amount
    }

def convert_transaction_data_to_bytes(transaction_data):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"]= str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["amount"] = str(transaction_data["amount"])
    return json.dumps(new_transaction_data,indent=2).encode('utf-8')


def Transaction_pool_address()->str:

    address="http://127.0.0.1:5001"
    url_parse = urlparse(address).netloc
    print(url_parse)
    return url_parse

Transaction_pool_address()

