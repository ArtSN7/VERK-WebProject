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

blueprint = flask.Blueprint('log_reg', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Log in')


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

            return redirect(f'/projects/{user.id}')

        return render_template('login.html', message='Wrong login or password', form=form)

    return render_template('login.html', title='Verk | Login', form=form)


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

        return redirect(f'/projects/{user.id}')

    return render_template('signup.html', title='Verk | Registration', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/base/<int:user_id>')
def base(user_id):
    # тут имя надо брать введенное пользователем, но я даун не знаю как это сделать, а щас уже разбираться поздно да и
    # я не соображу, поэтому чтобы без говнокода напишу заглушку. А еще нужно либо сделать выбор аватарки из
    # предложенных, либо как в лицее основывываясь на возрасте, но тогда нужно в регистрации добавить ввод возраста
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    print(LoginManager.user_loader)
    return render_template('base.html', title='Verk | Base', name=user.name, id=user_id)


@blueprint.route('/agenda/<int:user_id>')
def agenda(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('agenda.html', title='Verk | Agenda', name=user.name, id=user_id)


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


@blueprint.route('/tasks/<int:user_id>')
def tasks(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('tasks.html', title='Verk | Tasks', name=user.name, id=user_id)


@blueprint.route('/notifications/<int:user_id>')
def notifications(user_id):
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('notifications.html', title='Verk | Notifications', name=user.name, id=user_id)