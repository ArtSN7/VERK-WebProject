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

blueprint = flask.Blueprint('project_view', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
                   "/static/profile_pics/profile_pic_blue.png",
                   "/static/profile_pics/profile_pic_pink.png",
                   "/static/profile_pics/profile_pic_violet.png"]


@blueprint.route('/project_view/<int:user_id>/<int:project_id>', methods=['GET', 'POST'])
def project_view(user_id, project_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('project_view.html', user_id=user_id, project_id=project_id,
                           list_of_avatars=list_of_avatars, avatar=user.picture, name=user.name)
