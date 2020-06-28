
from flask import Flask,render_template, request, session, Response, redirect
import json
import time
import os,sys
os.popen('rm 128d_index.data 128d_index.index')

from datetime import datetime
from werkzeug.utils import secure_filename
from Algoritmos.extractFeatures import getFeatures
from Algoritmos.KNNsearch import KNNsearch
from Algoritmos.Init_Rtree import rtree
import Algoritmos.Init_Rtree
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

@app.route("/KNN/<method>/<K>", methods=['POST'])
def KNN(method,K):
    file= request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        #codigo de ariana
        data=getFeatures("imagenes/"+filename)
        #print(data)
        start=datetime.now()
        ans = KNNsearch(data,int(K),method)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        response=[] 
        for i in ans:
            dictionary={}
            dictionary['peso']=-i[0]
            dictionary['nombre']=i[1] 
            response.append(dictionary)
        time =(datetime.now()-start)
        print(time)
        response = response[::-1]
        return Response(json.dumps(response),mimetype="application/json")
    return "FAILED"

@app.route("/RTREE/<K>", methods=['POST'])
def RTREE(K):
    global rtree
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data=getFeatures("imagenes/"+filename)
        list_carac = []
        for i in data: 
            list_carac.append(i)
            list_carac.append(i)
        start=datetime.now()
        lres = list(rtree.nearest(coordinates=tuple(list_carac), num_results=int(K), objects = "raw"))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
        #print(lres)   
        time =(datetime.now()-start)
        print(time)
        return Response(json.dumps(lres),mimetype="application/json")
    return "FAILED"


@app.route('/queries')
def queries():
    return render_template('queries.html')


if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))


