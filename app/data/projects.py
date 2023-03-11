#тут тип нельзя было написать projects? что за бред челы ну вы совсем больные камон
#ну блин че за клиника але почему 2 класса project в двух разных файлах бум бум совсем вы 

import sqlalchemy
from sqlalchemy import ForeignKey
from .db_session import SqlAlchemyBase


class Project(SqlAlchemyBase):
    __tablename__ = 'taskwer'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    
    project = sqlalchemy.Column(ForeignKey('projects.id'), nullable=True)
    
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)