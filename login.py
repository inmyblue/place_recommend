from flask import Flask, Blueprint, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv


import certifi
import os
import jwt
import bcrypt


#환경변수 값 불러오기
load_dotenv()

#DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

login_bp = Blueprint('login', __name__)
app = Flask(__name__)

@login_bp.route('/')
def login():
    return render_template('login.html')

@login_bp.route('/register', methods=['POST'])
def register():
    reg_id = request.form['reg_id']
    reg_pwd = request.form['reg_pwd']
    reg_name = request.form['reg_name']

    sha_pwd = bcrypt.hashpw(reg_pwd.encode('UTF-8'),bcrypt.gensalt())

    id_chk = db.member.find_one({'member_id' : reg_id}, {'_id' : False})
    if id_chk :
        return jsonify({"msg" : "이미 가입된 ID입니다"})

    doc = {
        'member_id' : reg_id,
        'member_pw' : sha_pwd,
        'member_name' : reg_name
    }

    db.member.insert_one(doc)

    return jsonify({"msg" : "회원가입이 완료되었습니다"})
