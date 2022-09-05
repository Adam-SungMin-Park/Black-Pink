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


@app.route('/test')
def picture_get():
    all_picture = list(db.fansGallery.find({},{'_id': False}))

    print(jsonify(all_picture))


@app.route("/test", methods=["POST"])
def picture_post():
    image_receive = request.form['image_give']
    name_receive = request.form['name_give']
    pictures = list(db.fansGallery.find({}, {'_id': False}))
    count = len(pictures) + 1
    doc = {
        'id' : count,
        'name': name_receive,
        'image': image_receive
    }
    db.fansGallery.insert_one(doc)
    return jsonify({'msg': 'picture uploaded!'})

@app.route('/galleryDelete', methods = ["DELETE"])
def gallery_delete():
    imageId = int(request.form['id_give'])
    db.fansGallery.delete_one({'id':imageId})
    return jsonify({'msg':'deleted!'})


@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    allPost = list(db.fans.find({}))
    count = len(allPost)
    doc = {
        'id': count+1,
        'name': name_receive,
        'comment': comment_receive
    }
    db.fans.insert_one(doc)
    return jsonify({'msg': 'POSTED!'})


@app.route("/homework", methods=["GET"])
def homework_get():
    allFans = list(db.fans.find({}, {'_id': False}))
    return jsonify({'msg': allFans})


@app.route('/gallery', methods = ["GET"])
def gallery_show():
    pictures = list(db.fansGallery.find({}, {'_id': False}))
    return jsonify({'pic': pictures})


@app.route("/homeworkDelete", methods = ["DELETE"])
def comment_delete():
    id_receive = int(request.form['id_give'])
    db.fans.delete_one({'id': id_receive})
    return jsonify({'msg':'Deleted'})


@app.route('/homeworkUpdate', methods = ["PUT"])
def updateComment():
    id_receive = int(request.form['id_give'])
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    db.fans.update_one({'id':id_receive}, {'$set': {'name': name_receive, 'comment': comment_receive}})
    return jsonify({'msg':'updated comment'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
