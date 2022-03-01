from flask import Flask, render_template, request, jsonify, Blueprint
app = Flask(__name__)

from pymongo import MongoClient
import certifi

import requests
from bs4 import BeautifulSoup
import  os


register_bp = Blueprint('register', __name__)

mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.recommend_place

@register_bp.route('/')
def home():
   return render_template('Register.html')

@register_bp.route("/food", methods=["POST"])
def food_post():
    name_receive = request.form["name_give"]
    title_receive = request.form["title_give"]
    comment_receive = request.form["comment_give"]
    suggestion_receive = request.form["suggestion_give"]
    url = request.form["shop_give"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')



    foods = soup.select('body')

    for food in foods:
        shop = soup.select_one('meta[property="og:title"]')['content']
        address = food.select_one('main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(1) > td').text
        image = soup.select_one('meta[property="og:image"]')['content']
        menu = soup.select_one('main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(3)').text

    place_list = list(db.place.find({}, {'_id': False}))
    count =len(place_list) + 1

    doc = {
        'num': count,
        'name': name_receive,
        'title': title_receive,
        'shop': shop,
        'menu': menu,
        'comment': comment_receive,
        'suggestion': suggestion_receive,
        'image': image,
        'address':address,

    }

    db.place.insert_one(doc)
    return jsonify({'msg':'맛집 등록 완료!'})