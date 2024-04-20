import datetime
from data.users import User
from flask import Flask
from data import db_session
from data.ads import Ads

db_session.global_init("db/db_ads.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'

ads = Ads()
ads.id_user = 2
ads.id_game = 1
ads.name = 'Скин на лютоволка1'
ads.description = 'Продаю скин на лютоволка. Блаблаблаблаблаблабла'
ads.product_quantity = 2
ads.price = 1000
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()

ads = Ads()
ads.id_user = 1
ads.id_game = 1
ads.name = 'Скин на лютоволка2'
ads.description = 'Продаю скин на лютоволка. Блаблаблаблаблаблабла'
ads.product_quantity = 2
ads.price = 20000
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()

ads = Ads()
ads.id_user = 1
ads.id_game = 1
ads.name = 'Скин на лютоволка3'
ads.description = 'Продаю скин на лютоволка. Блаблаблаблаблаблабла'
ads.product_quantity = 2
ads.price = 5000000
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()

ads = Ads()
ads.id_user = 2
ads.id_game = 1
ads.name = 'Скин на лютоволка4'
ads.description = 'Продаю скин на лютоволка. Блаблаблаблаблаблабла'
ads.product_quantity = 2
ads.price = 10
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()

ads = Ads()
ads.id_user = 2
ads.id_game = 1
ads.name = 'Скин на лютоволка5'
ads.description = 'Продаю скин на лютоволка. Блаблаблаблаблаблабла'
ads.product_quantity = 2
ads.price = 500
db_sess = db_session.create_session()
db_sess.add(ads)
db_sess.commit()
