from flask import Flask, render_template
from pymongo import MongoClient
import certifi

#DB Configure
client = MongoClient('mongodb+srv://pre_project:soaktth11@cluster0.qgqev.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.recommend_place

#Flask App Setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':`
    app.run('0.0.0.0', port=5000, debug=True)