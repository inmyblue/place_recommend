from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

import certifi
import os

# Blueprint Load
from list import lists_bp
from login import login_bp
from view import view

#환경변수 값 불러오기
load_dotenv(find_dotenv())

#DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

#Flask App Setup
app = Flask(__name__)


#view.py
app.register_blueprint(blueprint=view)
app.register_blueprint(lists_bp, url_prefix='/lists')
app.register_blueprint(login_bp, url_prefix='/login')


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)