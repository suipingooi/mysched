from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
load_dotenv()

app = Flask(__name__)

#  Setup to Connect to MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'iifscDB'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


# index landing page - READ
@app.route('/')
def index():
    schedule = db.schedule.find()
    return render_template('index.template.html',
                           schedule=schedule)


# COACHES PAGE
# coaches listing - READ
@app.route('/coaches')
def coaches_list():

    # search by
    nrocnum = request.args.get('nroc_level')

    criteria = {}

    if nrocnum:
        criteria['nroc_level'] = {
            '$regex': nrocnum, '$options': 'i'
        }

    coaches = db.coaches.find(criteria, {
        'coach_lname': 1,
        'coach_fname': 1,
        'nroc_level': 1,
        'philosophy': 1,
        'coach_email': 1,
        'coach_phone': 1
    })

    return render_template('coach.template.html',
                           coaches=coaches)


# coaches add new - CREATE
@app.route('/coaches/add')
def add_newcoach():
    return render_template('form_newcoach.template.html')


@app.route('/coaches/add', methods=['POST'])
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

    return redirect(url_for('coaches_list'))


# coaches remove - DELETE
@app.route('/coaches/<coach_id>/delete')
def del_coach(coach_id):
    coach_to_delete = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    return render_template('validate_coach.template.html',
                           coach_to_delete=coach_to_delete)


@app.route('/coaches/<coach_id>/delete', methods=['POST'])
def process_delete_coach(coach_id):
    db.coaches.remove({
        '_id': ObjectId(coach_id)
    })
    return redirect(url_for('coaches_list'))


@app.route('/coaches/<coach_id>/update')
def update_coach(coach_id):
    coach_to_edit = db.coaches.find_one({
        '_id': ObjectId(coach_id)
    })
    return render_template('update_coach.template.html',
                           coach_to_edit=coach_to_edit)


@app.route('/coaches/<coach_id>/update', methods=['POST'])
def process_update_coach(coach_id):
    db.coaches.update_one({
        '_id': ObjectId(coach_id)
    }, {
        '$set': request.form
    })
    return redirect(url_for('coaches_list'))

# STUDENTS PAGE
# students listing - READ


@app.route('/students')
def students_list():

    # search by
    skatelvl = request.args.get('skate_level')

    criteria = {}

    if skatelvl:
        criteria['skate_level'] = {
            '$regex': skatelvl, '$options': 'i'
        }

    students = db.students.find(criteria, {
        'student_lname': 1,
        'student_fname': 1,
        'skate_level': 1,
    })

    return render_template('student.template.html',
                           students=students)


# students new - CREATE
@app.route('/students/add')
def newstudent_form():
    return render_template('form_newstudent.template.html')


@app.route('/students/add', methods=['POST'])
def add_newstudent():
    student_fname = request.form.get('student_fname')
    student_lname = request.form.get('student_lname')
    date_of_birth = request.form.get('date_of_birth')
    citizenship = request.form.get('citizenship')
    student_email = request.form.get('student_email')
    student_phone = request.form.get('student_phone')
    skate_level = request.form.get('skate_level')

    dob = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')

    db.students.insert_one({
        "student_fname": student_fname,
        "student_lname": student_lname,
        "date_of_birth": dob,
        "citizenship": citizenship,
        "student_email": student_email,
        "student_phone": student_phone,
        "skate_level": skate_level
    })

    return redirect(url_for('students_list'))


# rinks listing - READ
@ app.route('/rinks')
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
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
