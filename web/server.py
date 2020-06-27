from flask import Flask,render_template, request, session, Response, redirect
import json
import time
import os,sys
from datetime import datetime
from werkzeug.utils import secure_filename
from Algoritmos.extractFeatures import getFeatures
from Algoritmos.KNNsearch import KNNsearch
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

UPLOAD_FOLDER = '/home/cesar21456/Desktop/git/PC4BD2/web/imagenes' 
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/KNN/<method>/<K>", methods=['POST'])
def KNN(method,K):
    file= request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        #codigo de ariana
        data=getFeatures("imagenes/"+filename)
        print(data)
        ans = KNNsearch(data,int(K),method)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        response=[] 
        for i in ans:
            dictionary={}
            dictionary['peso']=i[0]
            dictionary['nombre']=i[1] 
            response.append(dictionary)
        return Response(json.dumps(response),mimetype="application/json")
    return "FAILED"

@app.route("/RTREE", methods=['POST'])
def RTREE():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))      
        return data
    return "FAILED"


@app.route('/queries')
def queries():
    return render_template('queries.html')


if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))


