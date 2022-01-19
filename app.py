from flask import Flask, request, redirect
from pymongo import MongoClient
from shortid import ShortId



app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')


client = MongoClient(app.config['DB_URL'])
db = client.pythondb
ulr_db = db["urls"]


@app.route('/', methods=['POST'])
def store_url():
    result = ''
    exists = ulr_db.find({'url': request.form['url']})
    if exists.count() > 0:
        result = 'http://127.0.0.1:5000/'+ str(exists[0]['short_id'])   
    else:
        url = request.form['url']
        sid=ShortId()
        short_id = sid.generate()
        ulr_db.insert_one({
            'url':str(url),
            'short_id':str(short_id)
        })
        result = 'http://127.0.0.1:5000/' + str(short_id) 

    return result

@app.route('/<id>', methods=['GET'])
def change(id):
    data = ulr_db.find_one({'short_id': id})
    return redirect(data['url'])


if __name__ == '__main__':
    app.run()