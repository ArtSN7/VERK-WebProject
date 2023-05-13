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

list_of_avatars = ["/static/profile_pics/profile_pic_peach.png",
                   "/static/profile_pics/profile_pic_blue.png",
                   "/static/profile_pics/profile_pic_pink.png",
                   "/static/profile_pics/profile_pic_violet.png"]
list_of_img = [
    "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    "https://images.unsplash.com/photo-1618472609777-b038f1f04b8d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
    "https://images.unsplash.com/photo-1618556450994-a6a128ef0d9d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
    "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80",
    "https://images.unsplash.com/photo-1618556658017-fd9c732d1360?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80",
    "https://images.unsplash.com/photo-1633596683562-4a47eb4983c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
    "https://images.unsplash.com/photo-1629948618343-0d33f97a3091?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
    "https://images.unsplash.com/photo-1631695161296-fb4daf40d3f9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80",
    "https://images.unsplash.com/photo-1629729802306-2c196af7eef5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80",
    "https://images.unsplash.com/photo-1642427749670-f20e2e76ed8c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80"]



def checking_users(users):
    db_session = session.create_session()
    answer = []

    for i in users.split(', '):
        try:
            user = db_session.query(User).filter(User.id == i).first()
            if not user.id:
               return []
            else:
                answer.append(str(user.id))
        except Exception:
            return "wrong"

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
        if check == "wrong":
            return render_template('adding_task.html', title='Adding Task', form=form,
                                   message="Error in users, please try again")

        if check == []:
            return render_template('adding_task.html', title='Adding Task', form=form,
                                   message="Some users were not found")

        if checking_users_in_pr(check, form.project.data):
            return render_template('adding_task.html', title='Adding Task', form=form,
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


@blueprint.route('/tasks', methods=['GET', 'POST'])
@login_required
def all_tasks():
    t = []
    db_session = session.create_session()
    user_id = flask_login.current_user.id
    user = db_session.query(User).get(user_id)
    try:
        tasks = user.tasks.split(", ")
    except Exception:
        tasks = []
    for i in tasks:
        task = db_session.query(Tasks).get(i)
        t.append(
            [task.description, task.project, ".".join(str(task.end_date).split()[0].split("-")[::-1]), task.status, int(task.id)])
        t.sort(key=lambda row: (row[4]))
    return render_template('all_tasks.html', title='All Task', tasks=t, list_of_avatars=list_of_avatars,
                           avatar=user.picture-1, name=user.name, id=user_id)
