# эта херня для этого, та херня для другого так пишите боже пожалуйста
# сверху чтобы разбираться куда мусор сортировать


import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    projects = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)

    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)

    picture = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def __repr__(self):
    return '<User{}>'.format(self.name)
