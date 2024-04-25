import datetime
from data.users import User
from flask import Flask
from data import db_session
from data.transactions import Transactions

db_session.global_init("db/db_ads.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'


transaction = Transactions()
transaction.game_name = 'Albion Online'
transaction.amount = 100
transaction.id_client = 1
transaction.id_seller = 2
transaction.status = 'Ожидание подтверждения'
db_sess = db_session.create_session()
db_sess.add(transaction)
db_sess.commit()
