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
from data.projects import Project
import flask_login

blueprint = flask.Blueprint('projects', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
                   "/static/profile_pics/profile_pic_blue.png",
                   "/static/profile_pics/profile_pic_pink.png",
                   "/static/profile_pics/profile_pic_violet.png"]


class EditForm(FlaskForm):
    title = StringField('Title', description='test')
    users = StringField('Users', description='test')
    description = StringField("Description", description='test')
    img = SelectField('img', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], description='test')
    submit = SubmitField('Edit')


@blueprint.route(f'/projects')
@login_required
def projects():
    user_id = flask_login.current_user.id
    db_session = session.create_session()
    # список ссылок на фото
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

    prj_list = []

    user = db_session.query(User).get(user_id)
    try:
        pr = user.projects.split(", ")
    except Exception:
        pr = []
    projects = []
    print(pr)
    for i in pr:
        proj = db_session.query(Project).get(i)
        projects.append(proj)
    print(projects)
    for i in projects:
        prj_list.append({'img': list_of_img[i.img - 1], 'title': i.title, 'description': i.description, 'id': i.id})

    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)

    return render_template('projects.html', title='Verk | Projects', name=user.name, id=user_id,
                           list_of_avatars=list_of_avatars, avatar=user.picture-1, projects=prj_list,
                           len=len(prj_list))


@blueprint.route(f'/project_edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_edit(project_id):
    user_id = flask_login.current_user.id
    db_session = session.create_session()
    project = db_session.query(Project).get(project_id)
    user = db_session.query(User).get(user_id)
    u = project.users.split(', ')
    if str(user_id) not in u:
        return redirect('/projects')
    form = EditForm()
    form.description.description = project.description
    form.img.description = project.img
    form.users.description = project.users
    form.title.description = project.description
    if form.validate_on_submit():
        if form.users.data != "" and form.users.data != project.users:
            u = project.users.split(', ')
            for i in u:
                us = db_session.query(User).get(int(i))
                pr = us.projects.split(", ")
                print(pr)
                ind = int(pr.index(str(project_id)))
                print(ind)
                del pr[ind]
                pr = ", ".join(pr)
                us.projects = pr
                db_session.merge(us)
                db_session.commit()
            for i in form.users.data.split(", "):
                us = db_session.query(User).get(int(i))
                pr = us.projects.split(", ")
                pr.append(str(project_id))
                pr = ", ".join(pr)
                us.projects = pr
                db_session.merge(us)
                db_session.commit()
            project.users = form.users.data
        if form.description.data != "":
            project.description = form.description.data
        if form.img.data != project.img:
            project.img = form.img.data
        if form.title.data != "":
            project.title = form.img.data
        db_session.merge(project)
        db_session.commit()
        return redirect("/projects")

    return render_template('project_edit.html', title='Verk | Projects', name=user.name, id=user_id,
                           list_of_avatars=list_of_avatars, avatar=user.picture-1, idit=project_id, form=form)
