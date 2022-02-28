from flask import Flask, Blueprint, render_template, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

import certifi
import os

#환경변수 값 불러오기
load_dotenv()

#DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

lists_bp = Blueprint('lists', __name__)
app = Flask(__name__)

@lists_bp.route('/')
def lists():
    return render_template('list.html')

@lists_bp.route('/load', methods=['GET'])
def list_load():
    db_list = list(db.place.find({}, {'_id' : False}))
    return jsonify({'lists' : db_list})