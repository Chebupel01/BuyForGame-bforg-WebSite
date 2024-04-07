import datetime
from data.users import User
from flask import Flask
from data import db_session
from data.games import Games

db_session.global_init("db/db_ads.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'


game = Games()
game.id_game = 0
game.game_name = 'Albion Online'
db_sess = db_session.create_session()
db_sess.add(game)
db_sess.commit()
