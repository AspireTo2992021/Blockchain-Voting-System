from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    print("Hello World")
app.run('0.0.0.0',5000)
