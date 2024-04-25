import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Transactions(SqlAlchemyBase):
    __tablename__ = 'transactions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_client = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    id_seller = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default='')

    # Явное указание внешних ключей и связей с таблицей users
    client = orm.relationship('User', foreign_keys=[id_client], backref='transactions_client')
    seller = orm.relationship('User', foreign_keys=[id_seller], backref='transactions_seller')
