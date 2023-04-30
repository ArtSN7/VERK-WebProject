# добавление задачи


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
import datetime

blueprint = flask.Blueprint('adding_task', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()
import flask_login


def checking_users(users):
    db_session = session.create_session()
    answer = []

    for i in users.split(', '):
        user = db_session.query(User).filter(User.id == i).first()
        if not user.id:
            return []
        else:
            answer.append(user.id)

    return answer


def checking_users_in_pr(check, pr_id):
    db_session = session.create_session()
    pr_users = db_session.query(Project).filter(Project.id == pr_id).first().users
    for i in check:
        if str(i) not in pr_users:
            return True

    return False


class AddingTaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])

    # img = SelectField('Image', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    users = StringField("Users' emails separated by commos and spaces", validators=[DataRequired()])

    end_date = DateTimeField("End date", validators=[DataRequired()], format="%Y-%m-%d")

    submit = SubmitField('ADD')

    project = SelectField("Project", validators=[DataRequired()], choices=[])


@blueprint.route('/adding_task', methods=['GET', 'POST'])
@login_required
def adding_task():
    db_session = session.create_session()
    form = AddingTaskForm()
    user_id = flask_login.current_user.id
    user = db_session.query(User).get(user_id)

    form.project.choices = db_session.query(User).get(user_id).projects.split(', ')

    if form.validate_on_submit():

        check = checking_users(form.users.data)

        if check == []:
            return render_template('adding_project.html', title='Adding Task', form=form,
                                   message="Some users were not found")

        if checking_users_in_pr(check, form.project.data):
            return render_template('adding_project.html', title='Adding Task', form=form,
                                   message="Some users are not in the project")

        if len(check) == 1:
            answ = check[0]
        else:
            answ = ', '.join(check)

        task = Tasks(
            description=form.description.data,
            start_date=datetime.date.today(),
            end_date=form.end_date.data,
            project=form.project.data,
            users=answ
        )
        db_session.add(task)
        db_session.commit()
        for i in form.users.data.split(', '):
            user = db_session.query(User).get(i)
            print(task.id)
            if user.tasks != "":
                user.tasks = f'{user.tasks}, {task.id}'
            else:
                user.tasks = task.id
            db_session.merge(user)
            db_session.flush()
            db_session.commit()

        return redirect(f'/projects')

    return render_template('adding_task.html', title='Adding Task', form=form)
