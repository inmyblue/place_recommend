from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

import certifi
import os
import jwt

# Blueprint Load
from list import lists_bp
from login import login_bp
from view import view
from Register import register_bp

# 환경변수 값 불러오기
load_dotenv()

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

# Flask App Setup
app = Flask(__name__)

#SECRET KEY
secret_key = os.getenv('SECRETKEY')

# view.py
app.register_blueprint(view, url_prefix='/view')
app.register_blueprint(lists_bp, url_prefix='/lists')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(register_bp, url_prefix='/register')


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    logged = "False"
    try:
        payload = jwt.decode(token_receive, secret_key, algorithms=['HS256'])
        user_name = db.member.find_one({'member_id' : payload['id']}, {'_id' : False})['member_name']
        logged = "True"
        return render_template('index.html', logged = logged, user_name = user_name)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', logged=logged)
    except jwt.exceptions.DecodeError:
        return render_template('index.html', logged = logged)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
