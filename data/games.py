import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_game = sqlalchemy.Column(sqlalchemy.Integer)
    game_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ads = orm.relationship('Ads', back_populates='game')