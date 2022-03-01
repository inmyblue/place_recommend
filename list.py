from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

import certifi
import os
import jwt

#환경변수 값 불러오기
load_dotenv()

#DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

lists_bp = Blueprint('lists', __name__)
app = Flask(__name__)

#SECRET KEY
secret_key = os.getenv('SECRETKEY')

@lists_bp.route('/')
def lists():
    token_receive = request.cookies.get('mytoken')
    logged = "False"
    try:
        payload = jwt.decode(token_receive, secret_key, algorithms=['HS256'])
        user_name = db.member.find_one({'member_id': payload['id']}, {'_id': False})['member_name']
        logged = "True"
        return render_template('list.html', logged=logged, user_name = user_name)
    except jwt.ExpiredSignatureError:
        return render_template('list.html', logged=logged)
    except jwt.exceptions.DecodeError:
        return render_template('list.html', logged=logged)

@lists_bp.route('/load', methods=['GET'])
def list_load():
    db_list = list(db.place.find({}, {'_id' : False}))
    return jsonify({'lists' : db_list})