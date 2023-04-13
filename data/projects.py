#table for projects

import sqlalchemy
from sqlalchemy import ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Project(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Project'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    
    tasks = sqlalchemy.Column(sqlalchemy.String, default='') # ID через запятую ( 1, 4, 5 и тд)
    
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True) # ID юзеров в проекте ( также через запятую )
    