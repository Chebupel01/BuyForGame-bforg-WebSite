from data.users import User
from flask import Flask
from data import db_session
from data.Ads import Ads

db_session.global_init("db/db_bforg.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

user = User()
user.surname = "Scott"
user.name = "Ridley"
user.age = 21
user.hashed_password = '1111'
user.set_password(user.hashed_password)
user.email = "scott_chief@mars.org"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()
