from data.users import User
from data.projects import Project
from data.tasks import Tasks
import data.db_session as session


def Del():
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    spis = [1, 2, 3, 4, 5, 6, 7]
    for i in spis:
        us = db_session.query(User).filter(User.id == i).first()
        
        db_session.delete(us)
        db_session.commit()
        
        
Del()