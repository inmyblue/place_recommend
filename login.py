from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

import jwt
import certifi
import os
import hashlib
import datetime


#환경변수 값 불러오기
load_dotenv()

app = Flask(__name__)

#DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

#SECRET KEY
secret_key = os.getenv('SECRETKEY')

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def login():
    token_receive = request.cookies.get('mytoken')
    logged = "False"
    try:
        payload = jwt.decode(token_receive, secret_key, algorithms=['HS256'])
        user_name = db.member.find_one({'member_id': payload['id']}, {'_id': False})['member_name']
        logged = "True"
        return render_template('login.html', logged=logged, user_name = user_name)
    except jwt.ExpiredSignatureError:
        return render_template('login.html', logged=logged)
    except jwt.exceptions.DecodeError:
        return render_template('login.html', logged=logged)

@login_bp.route('/register', methods=['POST'])
def register():
    reg_id = request.form['reg_id']
    reg_pwd = request.form['reg_pwd']
    reg_name = request.form['reg_name']

    sha_pwd = hashlib.sha256(reg_pwd.encode()).hexdigest()
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

@login_bp.route('/login_chk', methods=['POST'])
def login_chk():
    id = request.form['id']
    pwd = request.form['pwd']
    sha_pwd = hashlib.sha256(pwd.encode()).hexdigest() #비밀번호 암호화
    status = "SUCCESS"

    db_user = db.member.find_one({'member_id': id}, {'_id': False})

    if not db_user:
        return jsonify({"msg" : "가입된 ID가 없습니다", "status" : status})

    db_member = db.member.find_one({'member_id' : id, 'member_pw' : sha_pwd}, {'_id' : False})
    if db_member:
        payload = {
            'id' : id,
            'exp' : datetime.datetime.utcnow()+datetime.timedelta(seconds=60)
        }
        access_token = jwt.encode(payload, secret_key, algorithm='HS256')

        return jsonify({"msg" : "로그인 성공", "status" : status, 'access_token' : access_token})
    else :
        return jsonify({"msg" : "비밀번호를 다시 확인해주세요", "status" : status})