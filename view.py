from flask import Flask, Blueprint, render_template, jsonify, request
from pymongo import MongoClient

import json
from bson import json_util

import certifi
import os

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

# #Flask App Setup
view = Blueprint("view", __name__)
app = Flask(__name__)

num = 1


@view.route('/')
def views():
    return render_template('view.html')


@view.route('/load/', methods=["GET"])
def view_load():
    print(num)
    place = list(db.place.find({'num': num}))
    place = json.dumps(place, default=json_util.default)
    return jsonify({'place': place})
    # return render_template('view.html', place = place)