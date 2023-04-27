# file with registration and login


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
from data.projects import Project

blueprint = flask.Blueprint('agenda', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
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
        date = datetime.date.today() + datetime.timedelta(days=i)

        spis1.append(date)
        spis2.append((date.month, date.day, date.year))

    return (spis1,
            spis2)  # spis1 - это даты для проверки задач ; spis2 возвращает список
    # из кортежей, где 1 значение - месяц, 2 - день


def taking_tasks(user_id):
    session.global_init("db/blogs.db")
    db_sess = session.create_session()

    response = []

    for i in taking_dates()[0]:
        tasks = db_sess.query(Tasks).filter(Tasks.end_date == i, Tasks.users.like(f"%{str(user_id)},%")).all()

        response.append([i.description for i in tasks])

    return (response,
            taking_dates()[1])  # задачи и дни


@blueprint.route('/agenda/<int:user_id>')
def agenda(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)

    tasks, dates = taking_tasks(user_id)
    today = datetime.datetime.now()
    weekday = today.weekday()

    print(tasks)
    print(dates)
    days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь"]

    return render_template('agenda.html', title='Verk | Agenda', name=user.name, id=user_id,
                           list_of_avatars=list_of_avatars, avatar=user.picture, days=days, dates=dates,
                           months=months, tasks=tasks, len=len, curday=0, curmonth=0, weekday=weekday,
                           year_now=today.year)


@blueprint.route('/agenda/<int:user_id>/<int:date_id>')
def new_agenda(user_id, date_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)

    tasks, dates = taking_tasks(user_id)
    today = datetime.datetime.now()
    weekday = today.weekday()

    current_day = dates[date_id][1]
    current_month = dates[date_id][0]

    print(tasks)
    print(dates)
    print(current_day)
    print(current_month)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь"]

    return render_template('agenda.html', title='Verk | Agenda', name=user.name, id=user_id, days=days, dates=dates,
                           months=months, tasks=tasks, len=len, curday=current_day, curmonth=current_month,
                           curdate=date_id, weekday=weekday, year_now=today.year, list_of_avatars=list_of_avatars,
                           avatar=user.picture)
