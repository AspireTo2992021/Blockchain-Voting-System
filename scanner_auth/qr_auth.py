import numpy as np
from pyzbar.pyzbar import decode
import cv2

# Reading QR Code from an Image
img = cv2.imread("./flask/utils/qr1.png")
# print(img)
code = decode(img)
# print(code)

for barcode in decode(img):
    # print(barcode.data)  # in bytes
    text = barcode.data.decode('utf-8')
    # print(text)
    # print(barcode.rect)


# Scanning QR Code from Camera Feed
vid = cv2.VideoCapture(0)
vid.set(3, 640)
vid.set(4, 740)

with open("./flask/utils/auth.txt", 'r') as file:
    auth_list = file.read().strip()
    # print(auth_list)

while True:
    success, img = vid.read()
    for barcode in decode(img):
        text = barcode.data.decode('utf-8')
        # print(text)
        polygon_Points = np.array([barcode.polygon], np.int32)
        polygon_Points = polygon_Points.reshape(-1, 1, 2)
        rect_Points = barcode.rect
        cv2.polylines(img, [polygon_Points], True, (255, 255, 0), 5)
        cv2.putText(img, text, (rect_Points[0], rect_Points[1]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)
    cv2.imshow("Video", img)
    cv2.waitKey(1)




# while True:
#     success, img = vid.read()
#     for barcode in decode(img):
#         text = barcode.data.decode('utf-8')
#         text = str(text)
#         if text not in auth_list:
#             color = (0, 0, 255)
#             displaytext = "Unauthorised Access"
#         else:
#             color = (0, 255, 0)
#             displaytext = "Access Granted"
#         polygon_Points = np.array([barcode.polygon], np.int32)
#         polygon_Points = polygon_Points.reshape(-1, 1, 2)
#         rect_Points = barcode.rect
#         cv2.polylines(img, [polygon_Points], True, color, 3)
#         cv2.putText(img, displaytext, (rect_Points[0], rect_Points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
#     cv2.imshow("Video", img)
#     cv2.waitKey(1)

 