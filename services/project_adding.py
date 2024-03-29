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
from server import load_user
import flask_login

blueprint = flask.Blueprint('adding_project', __name__, template_folder='templates')

session.global_init("db/blogs.db")
db_session = session.create_session()


def checking_users(users):
    db_session = session.create_session()
    answer = []

    for i in users.data.split(', '):
        user = db_session.query(User).filter(User.id == i).first()
        try:
            if not user.id:
                return []
            else:
                answer.append(str(user.id))
        except Exception:
            return "wrong"

    return answer


class AddingJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    description = StringField('Description', validators=[DataRequired()])

    img = SelectField('img', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], description='test')

    # img = SelectField('Image', validators=[DataRequired()], choices=[('1', 'cat'), ('2', 'dog'), ('3', 'cow')])

    users = StringField("Users' швы separated by commas and spaces", validators=[DataRequired()])

    submit = SubmitField('ADD')


@blueprint.route('/adding_project', methods=['GET', 'POST'])
@login_required
def adding_project():
    user_id = flask_login.current_user.id
    form = AddingJobForm()
    db_session = session.create_session()

    if form.validate_on_submit():

        check = checking_users(form.users)

        if int(form.img.data) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Wrong image number")
        try:
            if check == []:
                return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Some users were not found")
            if len(check) == 1:
                answ = check[0]
            else:
                answ = ', '.join(check)

        except Exception:
            return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Error in users, please try again")
        if answ == "w, r, o, n, g":
            return render_template('adding_project.html', title='Adding Project', form=form,
                                   message="Error in users, please try again")


        project = Project(
            img=form.img.data,
            title=form.title.data,
            description=form.description.data,
            users=str(user_id) + ', ' + answ
        )
        db_session.add(project)
        db_session.commit()
        users = project.users.split(', ')
        user = db_session.query(User).get(user_id)
        if user.projects:
            new_projects = user.projects.split(', ') + [str(project.id)]
            user.projects = ', '.join(new_projects)
        else:
            user.projects = str(project.id)
        db_session.commit()
        for i in users:
            user = db_session.query(User).filter(User.id == i).first()
            new_projects = user.projects.split(', ')
            if str(project.id) not in new_projects:
                new_projects.append(str(project.id))
            user.projects = ', '.join(new_projects)
            db_session.commit()
        return redirect(f'/projects')
    return render_template('adding_project.html', title='Verk | Adding Project', form=form)
