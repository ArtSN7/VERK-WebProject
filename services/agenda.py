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
    
    return (spis1, spis2) # spis1 - это даты для проверки задач ; spis2 возвращает список из кортежей, где 1 значение - месяц, 2 - день


def taking_tasks(user_id):
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    
    response = []
    
    for i in taking_dates()[0]:
        
        tasks = db_session.query(Tasks).filter(Tasks.end_date == i, Tasks.users.like(f"%{str(user_id)}%")).all()
        
        
        if len(tasks) > 2:
            response.append((tasks[0].description, '...'))
        elif len(tasks) == 0:
            response.append(('', ''))
        else:
            response.append((tasks[0].description, tasks[1].description))
            
    return (response, taking_dates()[1]) #задачи и дни


@blueprint.route('/agenda/<int:user_id>')
def agenda(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    
    tasks, dates = taking_tasks(user_id)
    
    print(tasks)
    print(dates)
    
    return render_template('agenda.html', title='Verk | Agenda', name=user.name, id=user_id)