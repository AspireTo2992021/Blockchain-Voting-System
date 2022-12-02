# scan_QR_code,validate_QR_Code are main methods
import qrcode
import cv2
from Crypto.PublicKey import RSA


import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.cloud import storage
from google.oauth2 import service_account
# Init firebase with your credentials

key_file_path = "RequiredFiles/key.json"
download_file_path = "RequiredFiles/downloaded_file.txt"

cred = credentials.Certificate(key_file_path)
initialize_app(cred, {'storageBucket': 'project1-40e50.appspot.com'})





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
    img.save("medium.png")

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

#make_QR_code("pkey")

"""qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("fk")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="aqua")
img.save("medium.png")


img=cv2.imread("medium.png")
det=cv2.QRCodeDetector()
val, pts, st_code=det.detectAndDecode(img)
print(val)"""
