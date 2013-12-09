import os
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session, redirect, url_for, escape
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

app.secret_key = '*\xd6\xe8T\xd7\xdc9\xcb\xbb\x9e/\xc1\xf5\xbas\x94s\xb6,\xbaB\xfcS!'

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)