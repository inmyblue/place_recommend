from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://pre_project:soaktth11@cluster0.qgqev.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

doc = {
    'name':'bob',
    'age':27
}
db.sy.insert_one(doc)

@app.route('/')
def home():
    return render_template('register-page.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)