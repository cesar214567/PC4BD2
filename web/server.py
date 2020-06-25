from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import os,sys
from datetime import datetime
from werkzeug import secure_filename

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

UPLOAD_FOLDER = '/home/cesar21456/Desktop' 
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
            return "NOICE"
    return "NICE "


@app.route('/queries')
def queries():
    return render_template('queries.html')

@app.route('/query',methods=['POST'])
def query():
    c = json.loads(request.data)
    r_tweet = tweetg.get_tweet_by_id(c['ID'])
    tweet_json =  {}
    tweet_json['ID'] = str(r_tweet.id)
    tweet_json['text'] = r_tweet.text
    tweet_json['date'] = str(r_tweet.created_at)
    tweet_json['lang'] = r_tweet.lang
    list_tweets = []
    list_tweets.append(tweet_json)
    return Response(json.dumps(
            list_tweets),
            mimetype='application/json'
        )

@app.route('/busqueda',methods=['POST'])
def busqueda():
    start=datetime.now()
    c = json.loads(request.data)
    query = c["query"]
    K=c["K"]
    result = retrieve.executeQuery(query,int(K))
    time= (datetime.now()-start)
    print(time)
    list_tweets = []
    
    for id in result:
        tweet = tweetg.get_tweet_by_id(id[1])
        tweet_json =  {}
        tweet_json['ID'] = str(tweet.id)
        tweet_json['text'] = tweet.text
        tweet_json['date'] = str(tweet.created_at)
        tweet_json['lang'] = tweet.lang
        list_tweets.append(tweet_json)
    return Response(json.dumps(
            list_tweets),
            mimetype='application/json'
        )


@app.route('/eliminar',methods=['DELETE'])
def eliminar():
    global created_block
    os.system('rm *.txt')
    created_block = 0
    return  Response(json.dumps(
        { "Success" : 200 }), mimetype ='application/json'
    )

@app.route('/create',methods=['POST'])
def create():
    start=datetime.now()    
    global created_block
    c = json.loads(request.data)
    tema = c["tema"]
    N_tweets= c["n_tweets"]
    print(c)
    print(N_tweets)
    tweets = tweetg.get_tweets(tema,int(N_tweets))
    print("el tamano del array mandado es "+str(len(tweets)))
    time =(datetime.now()-start)
    print(time)
    start=datetime.now()
    if created_block:
        filters.addTweets(tweets)
    else:
        filters.initBlocks(tweets,int(c["blocksize"]))
        created_block = 1
    res = {}
    res["status"] = 200
    time =(datetime.now()-start)
    print(time)
    return Response(json.dumps(
        res), mimetype ='application/json'
    )

if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))


