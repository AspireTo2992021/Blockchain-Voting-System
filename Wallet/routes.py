
from flask import render_template, request
from forms import QRCodeData
import secrets
import cv2
import os
import qrcode

decoded_info = ""

@app.route("/")
def home():
    return render_template('layout.html')

@app.route("/genqr", methods=["POST", "GET"])
def genqr():
    form = QRCodeData()

    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data.data
            image_name = f"{secrets.token_hex(10)}.png"
            qr_location = f"{app.config['UPLOADED_PATH']}/{image_name}"

            try:
                my_qrcode = qrcode.make(str(data))
                my_qrcode.save(qr_location)
            except Exception as e:
                print(e)
            return render_template('qr_generated.html', image=image_name)
    else:
        return render_template('qr_generate.html', form=form)

# @app.route("/decqr")
# def decqr():
#     return render_template('qr_decode.html')


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
        print(val)
        
        os.remove(file_location)
        decoded_info = val
       
    else:
       return render_template("upload.html")

@app.route("/decoded")
def decoded():
    global decoded_info
    return render_template("decoded.html", data=decoded_info)

@app.route("/vote")
def vote():
    return render_template("vote.html")

@app.route("/not_eligible")
def not_eligible():
    return render_template("not_eligible.html")