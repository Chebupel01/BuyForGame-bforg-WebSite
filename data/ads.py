import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Ads(SqlAlchemyBase):
    __tablename__ = 'ads'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                            primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    id_game = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("games.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    product_quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    user = orm.relationship('User')
    game = orm.relationship('Games')
