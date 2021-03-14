from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
from datetime import date
import os
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'iifscDB'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


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
    flash("File for Coach CREATED")
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
    flash("File for Coach DELETED")
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
    flash("File for Coach UPDATED")
    return redirect(url_for('coaches_list'))


# STUDENTS
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
        'age': 1,
    })

    return render_template('student.template.html',
                           students=students)


@app.route('/students/add_newstudent')
def newstudent_form():
    return render_template('form_newstudent.template.html')


@app.route('/students/add_newstudent', methods=['POST'])
def add_newstudent():
    student_fname = request.form.get('student_fname')
    student_lname = request.form.get('student_lname')
    date_of_birth_day = request.form.get('date_of_birth_day')
    date_of_birth_month = request.form.get('date_of_birth_month')
    date_of_birth_year = request.form.get('date_of_birth_year')
    citizenship = request.form.get('citizenship').upper()
    student_email = request.form.get('student_email')
    student_phone = request.form.get('student_phone')
    skate_level = request.form.get('skate_level')

    date_of_birth = (date_of_birth_day +
                     date_of_birth_month +
                     date_of_birth_year)

    dob_dt = datetime.datetime.strptime(date_of_birth, '%d%m%Y')
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    cur_dt = datetime.datetime.strptime(today_str, '%Y-%m-%d')
    age_td = str(cur_dt - dob_dt)
    age_days_str = age_td.rstrip('days, 00:00:00')
    age_days_int = int(age_days_str)
    age = int(age_days_int // 365.2425)

    m = date_of_birth_month
    if m == "01":
        m = "JAN"
    elif m == "02":
        m = "FEB"
    elif m == "03":
        m = "MAR"
    elif m == "04":
        m = "APR"
    elif m == "05":
        m = "MAY"
    elif m == "06":
        m = "JUN"
    elif m == "07":
        m = "JUL"
    elif m == "08":
        m = "AUG"
    elif m == "09":
        m = "SEP"
    elif m == "10":
        m = "OCT"
    elif m == "11":
        m = "NOV"
    elif m == "12":
        m = "DEC"
    date_of_birth_month = m
    date_of_birth = (date_of_birth_day +
                     date_of_birth_month +
                     date_of_birth_year)

    db.students.insert_one({
        "student_fname": student_fname,
        "student_lname": student_lname,
        "date_of_birth": date_of_birth,
        "date_of_birth_day": date_of_birth_day,
        "date_of_birth_month": date_of_birth_month,
        "date_of_birth_year": date_of_birth_year,
        "age": age,
        "citizenship": citizenship,
        "student_email": student_email,
        "student_phone": student_phone,
        "skate_level": skate_level,
    })
    flash("File for Skater CREATED")
    return redirect(url_for('students_list'))


@ app.route('/students/<student_id>/skater')
def student_skater(student_id):
    student_to_show = db.students.find_one({
        '_id': ObjectId(student_id)
    })

    return render_template('skaterID.template.html',
                           student_to_show=student_to_show)


@ app.route('/students/<student_id>/form_competition')
def addcompetition_form(student_id):
    student_to_task = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('form_addcompetition.template.html',
                           student_to_task=student_to_task)


@ app.route('/students/<student_id>/form_competition', methods=['POST'])
def add_competition(student_id):
    db.students.find_one({
        '_id': ObjectId(student_id)
    })

    year = int(request.form.get('comp_year'))
    title = request.form.get('comp_title')
    category = request.form.get('comp_category')
    seq1 = request.form.get('comp_seq1')
    seq2 = request.form.get('comp_seq2')
    seq3 = request.form.get('comp_seq3')
    seq4 = request.form.get('comp_seq4')
    seq5 = request.form.get('comp_seq5')
    seq6 = request.form.get('comp_seq6')
    seq7 = request.form.get('comp_seq7')
    base = float(request.form.get('comp_base'))
    TES = float(request.form.get('comp_tes'))
    PCS = float(request.form.get('comp_pcs'))
    TSS = float(PCS + TES)

    db.students.update({
        '_id': ObjectId(student_id)
    }, {
        '$push': {
            "competition_data": [
                {
                    'comp_year': year,
                    'comp_title': title,
                    'category': category,
                    'seq1': seq1,
                    'seq2': seq2,
                    'seq3': seq3,
                    'seq4': seq4,
                    'seq5': seq5,
                    'seq6': seq6,
                    'seq7': seq7,
                    'base_value': base,
                    'TES': TES,
                    'PCS': PCS,
                    'TSS': TSS
                }
            ]
        }
    })

    flash("File for Skater UPDATED")
    return redirect(url_for('students_list'))


@ app.route('/students/<student_id>/delete')
def del_student(student_id):
    student_to_delete = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('validate_student.template.html',
                           student_to_delete=student_to_delete)


@ app.route('/students/<student_id>/delete', methods=['POST'])
def process_delete_student(student_id):
    db.students.remove({
        '_id': ObjectId(student_id)
    })
    flash("File for Student DELETED")
    return redirect(url_for('students_list'))


@ app.route('/students/<student_id>/update')
def update_student(student_id):
    student_to_edit = db.students.find_one({
        '_id': ObjectId(student_id)
    })

    return render_template('update_student.template.html',
                           student_to_edit=student_to_edit)


@ app.route('/students/<student_id>/update', methods=['POST'])
def process_update_student(student_id):
    db.students.update_one({
        '_id': ObjectId(student_id)
    }, {
        '$set': request.form
    })
    flash("File for Skater UPDATED")
    return redirect(url_for('students_list'))


# rinks listing - READ
@ app.route('/rinks')
def rinks_list():

    locreq = request.args.get('location')

    criteria = {}

    if locreq:
        criteria['location'] = {
            '$regex': locreq, '$options': 'i'
        }

    rinks = db.rinks.find(criteria, {
        'name': 1,
        'location': 1,
        'phone': 1,
        'address.unit': 1,
        'address.building': 1,
        'address.street': 1,
        'website': 1,
    })
    return render_template('rink.template.html',
                           rinks=rinks)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
