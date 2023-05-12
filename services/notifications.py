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

blueprint = flask.Blueprint('notifications', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
               "/static/profile_pics/profile_pic_blue.png",
               "/static/profile_pics/profile_pic_pink.png",
               "/static/profile_pics/profile_pic_violet.png"]


@blueprint.route('/notifications')
@login_required
def notifications():
    user_id = current_user.id
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('notifications.html', title='Verk | Notifications', name=user.name, user_id=user_id,
                           list_of_avatars=list_of_avatars, avatar=user.picture)

