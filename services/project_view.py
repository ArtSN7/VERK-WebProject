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
from services.agenda import taking_tasks

blueprint = flask.Blueprint('project_view', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
                   "/static/profile_pics/profile_pic_blue.png",
                   "/static/profile_pics/profile_pic_pink.png",
                   "/static/profile_pics/profile_pic_violet.png"]
list_of_img = [
        "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        "https://images.unsplash.com/photo-1618472609777-b038f1f04b8d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
        "https://images.unsplash.com/photo-1618556450994-a6a128ef0d9d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
        "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80",
        "https://images.unsplash.com/photo-1618556658017-fd9c732d1360?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
        "https://images.unsplash.com/photo-1633596683562-4a47eb4983c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
        "https://images.unsplash.com/photo-1629948618343-0d33f97a3091?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
        "https://images.unsplash.com/photo-1631695161296-fb4daf40d3f9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
        "https://images.unsplash.com/photo-1629729802306-2c196af7eef5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80",
        "https://images.unsplash.com/photo-1642427749670-f20e2e76ed8c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80"]


@blueprint.route('/project_view/<int:user_id>/<int:project_id>', methods=['GET', 'POST'])
def project_view(user_id, project_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    project = db_sess.query(Project).get(project_id)
    task_list = {}
    collab_list = []
    tasks, dates = taking_tasks(user_id)
    today = datetime.datetime.now()
    weekday = today.weekday()
    delta_time1 = datetime.timedelta(days=42)
    days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь"]
    if project.tasks:
        for i in project.tasks.split(', '):
            task = db_sess.query(Tasks).get(int(i))
            end = str(task.end_date).split()[0]
            end_date = datetime.date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
            print(end_date, today.date(), today.date() + delta_time1)
            for date_id in range(42):
                if today.date() <= end_date < today.date() + delta_time1 and date_id in task_list:
                    task_list[(end_date - today.date()).days].append({'description': task.description})
                elif today.date() <= end_date < today.date() + delta_time1:
                    task_list[(end_date - today.date()).days] = [{'description': task.description}]
    for i in project.users.split(', '):
        collaborator = db_sess.query(User).get(int(i))
        if int(i) != user_id:
            collab_list.append({'name': collaborator.name, 'img': list_of_avatars[collaborator.picture - 1]})
    return render_template('project_view.html', user_id=user_id, project_id=project_id, list_of_avatars=list_of_avatars,
                           avatar=user.picture, name=user.name, tasks=task_list, description=project.description,
                           title=project.title, img=list_of_img[project.img - 1], collaborators=collab_list, days=days,
                           dates=dates, months=months, len=len, curday=0, curmonth=0, weekday=weekday,
                           year_now=today.year, id=user.id)


@blueprint.route('/project_view/<int:user_id>/<int:project_id>/<int:date_id>', methods=['GET', 'POST'])
def project_view_new(user_id, project_id, date_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    project = db_sess.query(Project).get(project_id)
    task_list = {}
    collab_list = []
    tasks, dates = taking_tasks(user_id)
    today = datetime.datetime.now()
    weekday = today.weekday()
    current_day = dates[date_id][1]
    current_month = dates[date_id][0]
    delta_time1 = datetime.timedelta(days=42)
    days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь"]
    if project.tasks:
        for i in project.tasks.split(', '):
            task = db_sess.query(Tasks).get(int(i))
            end = str(task.end_date).split()[0]
            end_date = datetime.date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
            print(end_date, today.date(), today.date() + delta_time1)
            if today.date() <= end_date < today.date() + delta_time1 and date_id in task_list:
                task_list[(end_date - today.date()).days].append({'description': task.description})
            elif today.date() <= end_date < today.date() + delta_time1:
                task_list[(end_date - today.date()).days] = [{'description': task.description}]
    for i in project.users.split(', '):
        collaborator = db_sess.query(User).get(int(i))
        if int(i) != user_id:
            collab_list.append({'name': collaborator.name, 'img': list_of_avatars[collaborator.picture - 1]})
    print(task_list, date_id)
    return render_template('project_view.html', user_id=user_id, project_id=project_id, list_of_avatars=list_of_avatars,
                           avatar=user.picture, name=user.name, tasks=task_list, description=project.description,
                           title=project.title, img=list_of_img[project.img - 1], collaborators=collab_list, days=days,
                           dates=dates, months=months, len=len, curday=current_day, curmonth=current_month,
                           weekday=weekday, year_now=today.year, id=user.id, curdate=date_id)