# добавление проекта


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

blueprint = flask.Blueprint('adding_project', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()


def checking_users(users):
    db_session = session.create_session()
    answer = []

    for i in users.split(', '):
        user = db_session.query(User).filter(User.email == i).first()
        if not user.id:
            return []
        else:
            answer.append(user.id)

    return answer


class AddingJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    description = StringField('Description', validators=[DataRequired()])

    img = IntegerField('Image - one integer from 1 to 11', validators=[DataRequired()])

    # img = SelectField('Image', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    users = StringField("Users' emails separated by commos and spaces", validators=[DataRequired()])

    submit = SubmitField('ADD')


@blueprint.route('/adding_project/<int:user_id>', methods=['GET', 'POST'])
def adding_project(user_id):
    form = AddingJobForm()
    db_session = session.create_session()

    if form.validate_on_submit():

        check = checking_users(form.users)

        if form.img not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Wrong image number")

        if check == []:
            return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Some users were not found")

        if len(check) == 1:
            answ = check[0]
        else:
            answ = ', '.join(check)

        project = Project(
            img=form.img.data,
            title=form.title.data,
            description=form.description.data,
            users=answ
        )
        db_session.add(project)
        db_session.commit()

        return redirect(f'/projects/{user_id}')

    return render_template('adding_project.html', title='Verk | Adding Project', form=form)
