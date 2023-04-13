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



blueprint = flask.Blueprint('rpojects', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()



@blueprint.route(f'/projects/<int:user_id>')
def projects(user_id):
    prj_list = [{
        "img": "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=Mnw\
                    xMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        "title": "Codding"
    },
        {
            "img": "https://images.unsplash.com/photo-1618472609777-b038f1f04b8d?ixlib=rb-4.0.3&ixid=Mnw\
                    xMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
            "title": "Design"
        },
        {
            "img": "https://images.unsplash.com/photo-1618556450994-a6a128ef0d9d?ixlib=rb-4.0.3&ixid=Mnw\
            xMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
            "title": "Marketing"
        },
        {
            "img": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?ixlib=rb-4.0.3&ixid=Mnw\
            xMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80",
            "title": "Prototyping"
        },
    ]
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('projects.html', title='Verk | Projects', name=user.name, id=user_id, projects=prj_list)