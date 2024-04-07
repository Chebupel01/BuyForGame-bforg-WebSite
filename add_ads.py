import datetime
from data.users import User
from flask import Flask
from data import db_session
from data.ads import Ads

db_session.global_init("db/db_ads.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'


ads = Ads()
ads.id_user = 0
ads.id_game = 0
ads.text = 'sadddasdasdas'
ads.product_quantity = 0
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()
