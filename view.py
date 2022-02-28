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


@view.route('/')
def views():
    return render_template('view.html')
    # return "view test"


@view.route('/load', methods=["GET"])
def view_load():
    place = list(db.place.find({'num': 1}))
    place = json.dumps(place, default=json_util.default)
    return jsonify({'place': place})

