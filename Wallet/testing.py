from wallet import validate_signature
from wallet import Transaction
from wallet import initialize_wallet
from utils import scan_QR_code,validate_QR_Code ,convert_transaction_data_to_bytes
from Crypto.PublicKey import RSA

key_file_path = "RequiredFiles/key.json"
download_file_path = "RequiredFiles/downloaded_file.txt"

def test ():
    json = {"receiver_address " : "avs" ,"amount":1}
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
        #resp = send_to_pool(T.send_to_nodes())
        resp = T.send_to_nodes()
        print(validate_signature(resp["public_key"] ,  resp["signature"] , convert_transaction_data_to_bytes(resp["TransactionData"])))
   
    except Exception as e :
       print(f'Error from Wallet IN method in transaction ')
       
test()