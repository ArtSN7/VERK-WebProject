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
            answer.append(str(user.id))

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

    submit = SubmitField('ADD')

    project = SelectField("Project", validators=[DataRequired()], choices=[])


@blueprint.route('/adding_task/<int:date_id>', methods=['GET', 'POST'])
@login_required
def adding_task(date_id):
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

        delta_time1 = datetime.timedelta(days=date_id)
        task = Tasks(
            description=form.description.data,
            start_date=datetime.date.today(),
            end_date=datetime.datetime.today().date() + delta_time1,
            project=form.project.data,
            users=str(user_id) + ', ' + answ,
            status='scheduled'
        )
        db_session.add(task)
        db_session.commit()
        user = db_session.query(User).get(user_id)
        pr = db_session.query(Project).get(int(form.project.data))
        print(pr)
        if user.tasks:
            new_tasks = user.tasks.split(', ') + [str(task.id)]
            user.tasks = ', '.join(new_tasks)
        else:
            user.tasks = str(task.id)

        if pr.tasks:
            new_tasks = pr.tasks.split(', ') + [str(task.id)]
            pr.tasks = ', '.join(new_tasks)
        else:
            pr.tasks = str(task.id)
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

        return redirect(f'/project_view/{form.project.data}')

    return render_template('adding_task.html', title='Adding Task', form=form)
