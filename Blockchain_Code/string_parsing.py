# this file show hot to convert jsinify bytes and bring back nytes back from strings

from hashlib import scrypt
from os import urandom

from flask import jsonify
import json
secret = b'M\x13\xaf\x02\xc2\xe4\xec\x9e\xbe\xd7\xcbe^\xb8uX\xf2\xa0\xbc}\xddW\xd3\xf1\x9d5\x06\xc3\xdc\xc8\x86\x89\xd7\xf9\xc9\xffi/\x9a\xfe\xfc\x99\xd4#/~b"\x03\xe1>>\xaaj\x92\x00/\xcd}.:\xbcO\xba'
print(secret)
a=str(secret)
print("\n",a)
j={}

j["t"] = a
js= json.dumps(j)
print("\n", js)
print(type(js))

js=js.replace("\\\\",'\\' )
js=js[7:len(js)-1-1]

js=eval(js)

print("replaced js: \n")
print(js)
print(type(js))

print(js==secret)
