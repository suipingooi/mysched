from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#  Setup to Connect to MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'rink'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


# index landing page - READ

@app.route('/')
def index():
    schedule = db.schedule.find({}, {
        'datetime': 1,
        'ice_type': 1,
        'coach_id': 1,
        'students': 1
    })
    return render_template('index.template.html', schedule=schedule)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
