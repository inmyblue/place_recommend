from flask import Blueprint, render_template
# from pymongo import MongoClient
# import certifi
#
# #DB Configure
# client = MongoClient('mongodb+srv://pre_project:soaktth11@cluster0.qgqev.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
# db = client.recommend_place
#
# #Flask App Setup
view_test = Blueprint("view_test",__name__, url_prefix="/view")

# @view_test.route('/view')
@view_test.route('/')
def view():
    return render_template('view.html')
    # return "view test"

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)