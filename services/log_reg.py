# file with registration and login


import data.db_session as session
from data.users import User
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, logout_user, login_required, login_user
import datetime
import flask
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, SearchField, SelectField, IntegerField, \
    SelectFieldBase, DateTimeField, SelectMultipleField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from data.users import User

blueprint = flask.Blueprint('log_reg', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])

    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])

    # picture = SelectField('Picture', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    # сделать потом выбор picture из фозможных вариантов!

    submit = SubmitField('Sign up')


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_session = session.create_session()

    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email == form.email.data).first()
        pas = user.password

        if user and user.check_password(pas, form.password.data):
            login_user(user)

            return redirect('/base')

        return render_template('login.html', message='Wrong login or password', form=form)

    return render_template('login.html', title='Login', form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    db_session = session.create_session()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Registration', form=form,
                                   message="Passwords are not the same")

        if db_session.query(User).filter(User.email == form.email.data).first():
            return render_template('signup.html', title='Registration', form=form,
                                   message="Opps, the current email is already used")

        user = User(
            login=form.login.data,
            email=form.email.data,
            name=form.name.data,
            picture=1
        )
        user.set_password(form.password.data)
        user.password = user.password_hash
        db_session.add(user)
        db_session.commit()

        return redirect('/login')

    return render_template('signup.html', title='Registration', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/base')
def base():
    # тут имя надо брать введенное пользователем, но я даун не знаю как это сделать, а щас уже разбираться поздно да и
    # я не соображу, поэтому чтобы без говнокода напишу заглушку. А еще нужно либо сделать выбор аватарки из
    # предложенных, либо как в лицее основывываясь на возрасте, но тогда нужно в регистрации добавить ввод возраста
    return render_template('base.html', title='Base', name='Billy S.')


@blueprint.route('/agenda')
def agenda():
    return render_template('agenda.html', title='Agenda', name='Billy S.')


@blueprint.route('/projects')
def projects():
    return render_template('projects.html', title='Projects', name='Billy S.')


@blueprint.route('/tasks')
def tasks():
    return render_template('tasks.html', title='Tasks', name='Billy S.')


@blueprint.route('/notifications')
def notifications():
    return render_template('notifications.html', title='Notifications', name='Billy S.')
