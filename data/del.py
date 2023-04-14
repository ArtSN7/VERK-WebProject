from users import User
from projects import Project
from tasks import Tasks
import db_session as session


def Del_user():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    spis = [1, 2, 3, 4, 5]
    for i in spis:
        us = db_session.query(User).filter(User.id == i).first()
        
        db_session.delete(us)
        db_session.commit()
        
        
def Del_pr():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    spis = [1, 2, 3]
    for i in spis:
        us = db_session.query(Project).filter(Project.id == i).first()
        
        db_session.delete(us)
        db_session.commit()
        
        
def Del_task():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    spis = [1, 2, 3]
    for i in spis:
        us = db_session.query(Tasks).filter(Tasks.id == i).first()
        
        db_session.delete(us)
        db_session.commit()
        
        
Del_user()
Del_pr()
Del_task()