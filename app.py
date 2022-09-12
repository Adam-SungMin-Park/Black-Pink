from flask import Flask, render_template, request, jsonify
import uuid
from pymongo import MongoClient
from db import client

app = Flask(__name__)

db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


def genUUID():
    return str(uuid.uuid4().int)[30:]


@app.route("/test", methods=["POST"])
def picture_post():
    image_receive = request.form['image_give']
    name_receive = request.form['name_give']
    if  name_receive == "" or image_receive == "":
        return jsonify({'msg': 'fill in the form'})
    doc = {
        'id': genUUID(),
        'name': name_receive,
        'image': image_receive
    }
    db.fansGallery.insert_one(doc)
    return jsonify({'msg': 'picture uploaded!'})


@app.route('/galleryDelete', methods=["DELETE"])
def gallery_delete():
    imageId = request.form['id_give']
    db.fansGallery.delete_one({'id': imageId})
    return jsonify({'msg': 'deleted!'})


@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    if name_receive == "" or comment_receive == "":
        return jsonify({'msg': 'fill in the form'})

    doc = {
        'id': genUUID(),
        'name': name_receive,
        'comment': comment_receive
    }
    db.fans.insert_one(doc)
    return jsonify({'msg': 'POSTED!'})


@app.route("/homework", methods=["GET"])
def homework_get():
    allFans = list(db.fans.find({}, {'_id': False}))
    return jsonify({'msg': allFans, 'test': uuid.uuid4()})


@app.route('/gallery', methods=["GET"])
def gallery_show():
    pictures = list(db.fansGallery.find({}, {'_id': False}))
    return jsonify({'pic': pictures})


@app.route("/homeworkDelete", methods=["DELETE"])
def comment_delete():
    id_receive = request.form['id_give']
    print(id_receive)
    db.fans.delete_one({'id': id_receive})
    return jsonify({'msg': 'Deleted'})


@app.route('/galleryUpdate', methods=["PUT"])
def update_gallery():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']
    if id_receive == "" or name_receive == "" or url_receive == "":
        return jsonify({'msg': 'fill in the form'})
    db.fansGallery.update_one({'id': id_receive}, {'$set': {'name': name_receive, 'image': url_receive}})
    return jsonify({'msg': 'updated gallery!'})


@app.route('/homeworkUpdate', methods=["PUT"])
def updateComment():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    if id_receive == "" or name_receive == "" or comment_receive == "":
        return jsonify({'msg': 'Fill in the form!'})
    db.fans.update_one({'id': id_receive}, {'$set': {'name': name_receive, 'comment': comment_receive}})
    return jsonify({'msg': 'updated comment'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
