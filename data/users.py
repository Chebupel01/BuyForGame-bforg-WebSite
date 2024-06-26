import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    seller_rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_icon = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='default-icon.png')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    ads = orm.relationship('Ads', back_populates='user')



    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
