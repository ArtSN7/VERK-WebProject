# решили не делать из за бесполезности


import data.db_session as session
from data.users import User
from flask import Flask, redirect, render_template, request, g
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
import datetime
import flask
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, SearchField, SelectField, IntegerField, \
    SelectFieldBase, DateTimeField, SelectMultipleField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from data.users import User
from data.tasks import Tasks
import flask_login

blueprint = flask.Blueprint('tasks', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_img = ["/static/profile_pics/profile_pic_peach.png",
               "/static/profile_pics/profile_pic_blue.png",
               "/static/profile_pics/profile_pic_pink.png",
               "/static/profile_pics/profile_pic_violet.png"]


def taking_dates():
    today = datetime.date.today()

    spis1 = []
    spis2 = []

    spis1.append(today)
    spis2.append((today.month, today.day))

    for i in range(1, 42):
        Date = datetime.date.today() + datetime.timedelta(days=i)

        spis1.append(Date)
        spis2.append((Date.month, Date.day))

    return (spis1,
            spis2)  # spis1 - это даты для проверки задач ; spis2 возвращает список из кортежей, где 1 значение - месяц, 2 - день


def taking_tasks(user_id):
    session.global_init("db/blogs.db")
    db_session = session.create_session()

    today_date = taking_dates()[0][0]
    tasks_for_today = db_session.query(Tasks).filter(Tasks.end_date == today_date,
                                                     Tasks.users.like(f"%{str(user_id)},%")).all()

    tom_date = taking_dates()[0][1]
    tasks_for_tom = db_session.query(Tasks).filter(Tasks.end_date == tom_date,
                                                   Tasks.users.like(f"%{str(user_id)},%")).all()

    tasks_for_other = db_session.query(Tasks).filter(Tasks.end_date != tom_date, Tasks.end_date != today_date,
                                                     Tasks.users.like(f"%{str(user_id)},%")).all()

    return tasks_for_today, tasks_for_tom, tasks_for_other  # возвращает 1 - задачи на сегодня, 2 - на завтра, 3 - на остальные даты


@blueprint.route('/tasks')
@login_required
def tasks():
    user_id = flask_login.current_user.id
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('tasks.html', title='Verk | Tasks', name=user.name, id=user_id, list_of_img=list_of_img,
                           avatar=user.picture)
