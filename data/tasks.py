#тут тип нельзя было написать projects? что за бред челы ну вы совсем больные камон
#ну блин че за клиника але почему 2 класса project в двух разных файлах бум бум совсем вы 

import sqlalchemy
from sqlalchemy import ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Tasks(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    
    project = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) #к которому он привязан
    
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True) #описание задачи
    
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True) # ID людей, которые отвечают за задачу ( 1, 4, 6 и тд)
    
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)