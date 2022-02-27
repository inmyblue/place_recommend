from flask import Flask, Blueprint, render_template, jsonify
from pymongo import MongoClient
import certifi

#DB Configure
client = MongoClient('mongodb+srv://pre_project:soaktth11@cluster0.qgqev.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.recommend_place

lists_bp = Blueprint('lists', __name__)
app = Flask(__name__)

@lists_bp.route('/')
def lists():
    return render_template('list.html')

@lists_bp.route('/load', methods=['GET'])
def list_load():
    db_list = list(db.place.find({}, {'_id' : False}))
    print(db_list)
    return jsonify({'lists' : db_list})