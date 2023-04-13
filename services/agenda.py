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
from funcs import load_user


blueprint = flask.Blueprint('agenda', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()


@blueprint.route('/agenda/<int:user_id>')
def agenda(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('agenda.html', title='Verk | Agenda', name=user.name, id=user_id)