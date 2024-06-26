from data.users import User
from flask import Flask
from data import db_session
from data.ads import Ads

db_session.global_init("db/db_ads.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

user = User()
user.nickname = "Ridley"
user.admin = True
user.hashed_password = '1111'
user.set_password(user.hashed_password)
user.seller_rating = 5
user.email = "scott_chief@mars.org"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()

user = User()
user.nickname = "Maikov"
user.hashed_password = '1111'
user.set_password(user.hashed_password)
user.email = "artem123@mars.org"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()

user = User()
user.nickname = "Nikonorof"
user.hashed_password = '1111'
user.set_password(user.hashed_password)
user.email = "vasya123@mars.org"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()

user = User()
user.nickname = "Dmitry"
user.hashed_password = '1111'
user.set_password(user.hashed_password)
user.email = "flyer332@mars.org"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()