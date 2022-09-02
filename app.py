from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.o2cbi29.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_receive,
        'comment':comment_receive
    }
    db.fans.insert_one(doc);
    return jsonify({'msg':'POSTED!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    allFans = list(db.fans.find({},{'_id': False}))
    return jsonify({'msg': allFans})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
