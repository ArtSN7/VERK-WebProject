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


def checking_users(users):
    db_session = session.create_session()
    answer = []

    for i in users.data.split(', '):
        user = db_session.query(User).filter(User.email == i).first()
        if not user:
            return []
        else:
            answer.append(str(user.id))

    return answer


def checking_users_in_pr(check):
    db_session = session.create_session()
    pr_users = db_session.query(Project).filter(Project.id == i).first().users
    for i in check:
        if i not in pr_users:
            return True

    return False


class AddingTaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])

    # img = SelectField('Image', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    # users = StringField("Users' emails separated by commos and spaces", validators=[DataRequired()])

    # end_date = DateTimeField("End date", validators=[DataRequired()], format="%Y-%m-%d")

    submit = SubmitField('ADD')


@blueprint.route('/adding_task/<int:user_id>/<int:project_id>/<int:date_id>', methods=['GET', 'POST'])
def adding_task(user_id, project_id, date_id):
    form = AddingTaskForm()
    db_session = session.create_session()

    if form.validate_on_submit():

        # check = checking_users(form.users)
        #
        # if check == []:
        #     return render_template('adding_project.html', title='Adding Task', form=form,
        #                            message="Some users were not found")

        # if checking_users_in_pr(check):
        #     return render_template('adding_project.html', title='Adding Task', form=form,
        #                            message="Some users are not in the project")
        #
        # if len(check) == 1:
        #     answ = check[0]
        # else:
        #     answ = ', '.join(check)
        delta_time1 = datetime.timedelta(days=date_id)
        task = Tasks(
            description=form.description.data,
            start_date=datetime.date.today(),
            end_date=datetime.datetime.today().date() + delta_time1
        )
        db_session.add(task)
        db_session.commit()
        project = db_session.query(Project).get(project_id)
        new_tasks = project.tasks.split(', ') + [str(task.id)]
        project.tasks = ', '.join(new_tasks)
        db_session.commit()
        print(project.tasks)
        return redirect(f'/projects/{user_id}')

    return render_template('adding_task.html', title='Adding Task', form=form)
