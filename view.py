from flask import Flask, Blueprint, render_template, jsonify, request
from pymongo import MongoClient

import certifi
import os

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

app = Flask(__name__)
# #Flask App Setup
view = Blueprint("view", __name__)


@view.route('/')
def views():
    return render_template('view.html')

@view.route('/detail', methods=['GET'])
def view_detail():
    num = request.args.get('num')
    place = db.place.find_one({'num': int(num)}, {'_id' : False})
    return jsonify({'msg':'연결완료', 'place' : place})