from flask import Flask
import os
from flask_dropzone import Dropzone

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

app.config['SECRET_KEY'] = 'bf9b1b2111ab03c26782b1e7da3fd366fc5e127b'

app.config.update(
    UPLOADED_PATH=os.path.join(dir_path, 'static'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1
)
app.config['DROPZONE_REDIRECT_VIEW'] = 'decoded'

dropzone = Dropzone(app)


from application import routes