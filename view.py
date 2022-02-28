from flask import Blueprint, render_template, jsonify, request
from pymongo import MongoClient
import certifi
import json
from bson import json_util

# DB Configure
client = MongoClient(
    'mongodb+srv://pre_project:soaktth11@cluster0.qgqev.mongodb.net/Cluster0?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.recommend_place

# #Flask App Setup
view = Blueprint("view", __name__, url_prefix="/view")


# @view_test.route('/view')
@view.route('/')
def view_load():
    return render_template('view.html')
    # return "view test"


@view.route('/load', methods=["GET"])
def view_detail():
    place = list(db.place.find({'num': 2}))
    place = json.dumps(place, default=json_util.default)
    return jsonify({'place': place})

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
