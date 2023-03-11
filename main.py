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

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])

    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])

    # picture = SelectField('Picture', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    # сделать потом выбор picture из фозможных вариантов!

    submit = SubmitField('Register')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/main')

        return render_template('login.html', message='Wrong login or password', form=form)

    return render_template('login.html', title='Login', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    db_session = session.create_session()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Registration', form=form,
                                   message="Passwords are not the same")

        if db_session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Registration', form=form,
                                   message="Opps, the current email is already used")

        user = User(
            login=form.login.data,
            password=form.password.data,
            email=form.email.data,
            name=form.name.data,
            picture=1
        )

        db_session.add(user)
        db_session.commit()

        return redirect('/login')

    return render_template('registration.html', title='Registration', form=form)


@app.route('/main')
@login_required
def main():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    session.global_init("db/blogs.db")
    db_session = session.create_session()

    app.run(port=8080, host='127.0.0.1')
