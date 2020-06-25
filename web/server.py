from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import os,sys
from datetime import datetime
from werkzeug.utils import secure_filename


created_block = 0
db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

UPLOAD_FOLDER = '/home/enrique/Documentos/BD2/PC4BD2/web/imagenes' 
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def nani():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Success"
    return "NICE "


@app.route('/queries')
def queries():
    return render_template('queries.html')


if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))


