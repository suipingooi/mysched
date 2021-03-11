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
    schedule = db.schedule.find()
    return render_template('index.template.html',
                           schedule=schedule)


# coaches listing - READ
@app.route('/coaches')
def coaches_list():
    coaches = db.coaches.find()
    return render_template('coach.template.html',
                           coaches=coaches)


# coaches new - CREATE
@app.route('/coaches/add')
def add_newcoach():
    return render_template('form_newcoach.template.html')


@app.route('/coaches/add', methods=["POST"])
def newcoach_form():
    coach_fname = request.form.get('coach_fname')
    coach_lname = request.form.get('coach_lname')
    nroc_level = request.form.get('nroc_level')
    coach_email = request.form.get('coach_email')
    coach_phone = request.form.get('coach_phone')
    philosophy = request.form.get('philosophy')

    db.coaches.insert_one({
        "coach_fname": coach_fname,
        "coach_lname": coach_lname,
        "nroc_level": nroc_level,
        "coach_email": coach_email,
        "coach_phone": coach_phone,
        "philosophy": philosophy
    })

    return "New Coach Added"


# students listing - READ
@app.route('/students')
def students_list():
    skaters = db.skaters.find()
    return render_template('student.template.html',
                           skaters=skaters)


# students new - CREATE
@app.route('/students/add')
def newstudent_form():
    return render_template('form_newstudent.template.html')


@app.route('/students/add', methods=["POST"])
def add_newstudent():
    student_fname = request.form.get('student_fname')
    student_lname = request.form.get('student_lname')
    date_of_birth = request.form.get('date_of_birth')
    citizenship = request.form.get('citizenship')
    student_email = request.form.get('student_email')
    student_phone = request.form.get('student_phone')
    skate_level = request.form.get('skate_level')

    db.students.insert_one({
        "student_fname": student_fname,
        "student_lname": student_lname,
        "date_of_birth": date_of_birth,
        "citizenship": citizenship,
        "student_email": student_email,
        "student_phone": student_phone,
        "skate_level": skate_level
    })

    return "New Student Added"


# rinks listing - READ
@app.route('/rinks')
def rinks_list():
    rinks = db.rinks.find({}, {
        'rink': 1,
        'address': 1,
        'website': 1
    })
    return render_template('rink.template.html',
                           rinks=rinks)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
