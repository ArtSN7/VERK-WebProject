# file with registration and login
import flask_login

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

blueprint = flask.Blueprint('profile', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()

list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
                   "/static/profile_pics/profile_pic_blue.png",
                   "/static/profile_pics/profile_pic_pink.png",
                   "/static/profile_pics/profile_pic_violet.png"]


class EditForm(FlaskForm):
    password = PasswordField('Password')
    password_again = PasswordField('Password again')
    email = EmailField('Почта', description='test')
    name = StringField('Имя', description='test')
    phone = StringField('Телефон', description='test')
    birth_date = StringField('Дата рождения', description='test')
    bio = StringField('О себе', description='test')
    picture = SelectField('Status', choices=[1, 2, 3, 4], description='test')
    submit = SubmitField('Edit')


@blueprint.route('/profile')
@login_required
def profile():
    user_id = flask_login.current_user.id
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    return render_template('profile.html', title='Verk | Profile', name=user.name, id=user_id, email=user.email,
                           list_of_avatars=list_of_avatars, avatar=user.picture-1, phone=user.phone,
                           birth_date=str(user.birth_date).split()[0], bio=user.bio)


@blueprint.route('/profile/<int:user_id>')
@login_required
def profile1(user_id):
    u = flask_login.current_user.id
    if u == user_id:
        return redirect('/profile')
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    us = db_sess.query(User).get(u)
    return render_template('profile_foreign.html', title='Verk | Profile', name=us.name, naming=user.name, id=user_id, email=user.email,
                           list_of_avatars=list_of_avatars, avatar=us.picture-1, phone=user.phone, ava=user.picture-1,
                           birth_date=str(user.birth_date).split()[0], bio=user.bio)


@blueprint.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user_id = flask_login.current_user.id
    db_sess = session.create_session()
    user = db_sess.query(User).get(user_id)
    form = EditForm()
    form.phone.description = user.phone
    form.name.description = user.name
    form.birth_date.description = str(user.birth_date).split()[0]
    form.bio.description = user.bio
    form.picture.description = user.picture
    form.email.description = user.email
    if form.validate_on_submit():
        if form.email.data and db_session.query(User).filter(User.email == form.email.data).first():
            return render_template('profile_update.html', title='Verk | Profile', name=user.name, email=user.email,
                                   phone=user.phone, message="This email is already used", form=form,
                                   list_of_avatars=list_of_avatars, avatar=user.picture)
        elif form.phone.data and db_session.query(User).filter(User.phone == form.phone.data).first():
            return render_template('profile_update.html', title='Verk | Profile', name=user.name, email=user.email,
                                   phone=user.phone, message="This phone is already used", form=form,
                                   list_of_avatars=list_of_avatars, avatar=user.picture)
        elif (form.password.data or form.password_again.data) and form.password.data != form.password_again.data:
            return render_template('profile_update.html', title='Verk | Profile', name=user.name, email=user.email,
                                   phone=user.phone, message="Passswords are not the same", form=form,
                                   list_of_avatars=list_of_avatars, avatar=user.picture)

        if form.name.data != "":
            user.name = form.name.data
        if form.phone.data != "":
            user.phone = form.phone.data
        if form.birth_date.data != "":
            try:
                data = form.birth_date.data.split('.')
                user.birth_date = datetime.datetime(int(data[2]), int(data[1]), int(data[0]))
            except Exception:
                return render_template('profile_update.html', title='Verk | Profile', name=user.name, email=user.email,
                                       phone=user.phone, form=form, list_of_avatars=list_of_avatars,
                                       avatar=user.picture,
                                       birth_date=str(user.birth_date).split()[0], bio=user.bio, id=user_id, message="Wrong format of date, try dd-mm-yyyy")
        if form.email.data != "":
            user.email = form.email.data
        if form.bio.data != "":
            user.bio = form.bio.data
        if form.password.data != "":
            user.set_password(form.password.data)
            user.password = user.password_hash
        if form.picture.data != user.picture:
            user.picture = form.picture.data
        db_session.merge(user)
        db_session.flush()
        db_session.commit()

        return redirect(f'/projects')
    return render_template('profile_update.html', title='Verk | Profile', name=user.name, email=user.email,
                           phone=user.phone, form=form, list_of_avatars=list_of_avatars, avatar=user.picture-1,
                           birth_date=str(user.birth_date).split()[0], bio=user.bio, id=user_id)
