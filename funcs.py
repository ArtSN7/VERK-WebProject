import data.db_session as session
from data.users import User
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, logout_user, login_required, login_user
import datetime
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, SearchField, SelectField, IntegerField, \
    SelectFieldBase, DateTimeField, SelectMultipleField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from data.users import User
from services import log_reg, tasks, projects, notifications, agenda, project_adding, task_adding, profile, project_view

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


if __name__ == '__main__':
    session.global_init("db/blogs.db")
    db_session = session.create_session()

    # reg, login, logout ; after success a person will be redirected to the main (/main)

    app.register_blueprint(log_reg.blueprint)
    # app.register_blueprint(tasks.blueprint)
    app.register_blueprint(agenda.blueprint)
    app.register_blueprint(projects.blueprint)
    app.register_blueprint(notifications.blueprint)
    app.register_blueprint(project_adding.blueprint)
    app.register_blueprint(task_adding.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(project_view.blueprint)

    app.run(port=8080, host='127.0.0.1')
