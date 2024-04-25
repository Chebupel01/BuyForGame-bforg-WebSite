import os

import requests
from sqlalchemy.orm import joinedload
from waitress import serve
import datetime
from flask_restful import Api

from data.add_balance import AddBalanceForm
from data.add_gameform import AddGameForm
from data.ads import Ads
from data.games import Games
from data.message_form import MesForm
from data.product_placement import AddProductForm
from data.product_quantity import ProQForm
from data.upload_photo_form import UploadForm
from data.users import User
from data.login_form import LoginForm
from data.reg_form import RegForm
from flask import Flask, render_template, redirect, request, url_for, current_app
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, current_user
from data import db_session
from data import ads_api
from sqlalchemy import asc, desc
from data import user_api as users_resource

application = Flask(__name__)
application.config['SECRET_KEY'] = 'bforg-site_secret_key'
UPLOAD_FOLDER = 'static/images/users-icons'
UPLOAD_FOLDER1 = 'static/images/games-icons'
UPLOAD_FOLDER2 = 'static/images/users-products'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
application.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
api = Api(application)
login_manager = LoginManager()
login_manager.init_app(application)
db_session.global_init('db/db_ads.db')
api.add_resource(users_resource.UsersListResource, '/api/users')
api.add_resource(users_resource.UsersResource, '/api/user/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.route('/')
def home():
    print(123)
    return render_template('home.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    if form.validate_on_submit() and form.email.data in [user.email for user in users]:
        return render_template('registration.html', title='Зарегистрироваться',
                               form=form, message='Существующая почта')
    if form.validate_on_submit() and form.password.data != form.password_2.data:
        return render_template('registration.html', title='Зарегистрироваться',
                               form=form, message='разные пароли')
    if form.validate_on_submit() and form.password.data == form.password_2.data:
        db_sess = db_session.create_session()
        user = User()
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.set_password(user.hashed_password)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Зарегистрироваться',
                           form=form)


@application.route('/store', methods=['GET', 'POST'])
def store():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    games = [[game.game_name, game.id] for game in games]
    games.sort(key=lambda x: x[0])
    return render_template('store.html', games=games)


@application.route('/store/<int:id>')
def products(id):
    store_format = request.args.get('store_format')
    sort_by = request.args.get('sort_by')
    ads = Ads()
    db_sess = db_session.create_session()
    game = db_sess.query(Games).filter(Games.id == id).first()
    if sort_by == 'price_asc':
        products = db_sess.query(Ads).filter(Ads.id_game == id).order_by(asc(Ads.price)).all()
    elif sort_by == 'price_desc':
        products = db_sess.query(Ads).filter(Ads.id_game == id).order_by(desc(Ads.price)).all()
    elif sort_by == 'date_added':
        products = db_sess.query(Ads).filter(Ads.id_game == id).order_by(desc(Ads.date)).all()
    elif sort_by == 'seller_rating':
        products = db_sess.query(Ads).join(User).filter(Ads.id_game == id).order_by(desc(User.seller_rating)).all()
    return render_template('products.html', ads=ads, game=game, sort_by=sort_by, store_format=store_format,
                           products=products)


@application.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
    form = MesForm()
    form1 = ProQForm()
    db_sess = db_session.create_session()
    product = db_sess.query(Ads).filter(Ads.id == id).first()
    message = form.message.data
    amount = request.args.get('amount')
    print(form1.amount.data)
    try:
        directory = os.path.join(os.getcwd(), 'static', 'chats')
        users = [current_user.id, product.user.id]
        filename = f'{min(users)}-{max(users)}.txt'
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            messages = file.readlines()
    except Exception:
        messages = []
    if message:
        directory = os.path.join(os.getcwd(), 'static', 'chats')
        filename = f'{min(users)}-{max(users)}.txt'
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                messages = file.readlines()
            with open(filepath, "w", encoding='utf-8') as file:
                messages.append(f'cur:{current_user.id}:' + message + '\n')
                file.writelines(messages)
        except Exception:
            with open(filepath, "a+", encoding='utf-8') as file:
                file.write(f'cur:{current_user.id}:' + message + '\n')
                messages = [f'cur:{current_user.id}:' + message + '\n']
    form.message.data = ''

    return render_template('product.html', product=product, message=message, messages=messages[::-1],
                           form=form, form1=form1)


@application.route('/chats')
def chats():
    directory = os.path.join(current_app.root_path, 'static', 'chats')
    files = os.listdir(directory)
    chats = []
    db_sess = db_session.create_session()
    for file in files:
        file_name = file
        file = file.split('.')
        if int(file[0].split('-')[0]) == current_user.id or int(file[0].split('-')[1]) == current_user.id:
            ids = [int(file[0].split('-')[0]), int(file[0].split('-')[1])]
            ids.remove(current_user.id)
            ids = int(ids[0])
            user = db_sess.query(User).filter(User.id == ids).first()
            filepath = directory + '/' + file_name
            with open(filepath, 'r', encoding='utf-8') as file:
                messages = file.readlines()
            if messages:
                chats.append(
                    [datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d %B %Y %H:%M"), user,
                     messages[-1].split(':', 2)[-1], int(messages[-1].split(':', 2)[1]),
                     ids])
        chats.sort(key=lambda x: x[0], reverse=True)
    print(chats)
    return render_template('chats.html', chats=chats)


@application.route('/chat/<int:id>', methods=['GET', 'POST'])
def chat(id):
    messages = []
    form = MesForm()
    db_sess = db_session.create_session()
    product = db_sess.query(Ads).options(joinedload(Ads.user)).filter(Ads.id == id).first()
    message = form.message.data
    if message:
        users = [current_user.id, id]
        directory = os.path.join(os.getcwd(), 'static', 'chats')
        filename = f'{min(users)}-{max(users)}.txt'
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            messages = file.readlines()
        with open(filepath, "w", encoding='utf-8') as file:
            messages.append(f'cur:{current_user.id}:' + message + '\n')
            file.writelines(messages)
    else:
        directory = os.path.join(os.getcwd(), 'static', 'chats')
        users = [current_user.id, id]
        filename = f'{min(users)}-{max(users)}.txt'
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            messages = file.readlines()
    current_url = request.url
    form.message.data = ''
    directory = os.path.join(current_app.root_path, 'static', 'chats')
    files = os.listdir(directory)
    chats = []
    db_sess = db_session.create_session()
    for file in files:
        file_name = file
        file = file.split('.')
        if int(file[0].split('-')[0]) == current_user.id or int(file[0].split('-')[1]) == current_user.id:
            ids = [int(file[0].split('-')[0]), int(file[0].split('-')[1])]
            ids.remove(current_user.id)
            ids = int(ids[0])
            user = db_sess.query(User).filter(User.id == ids).first()
            filepath = directory + '/' + file_name
            with open(filepath, 'r', encoding='utf-8') as file:
                messages1 = file.readlines()
            if messages1:
                chats.append(
                    [datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d %B %Y %H:%M"), user,
                     messages1[-1].split(':', 2)[-1], int(messages1[-1].split(':', 2)[1]),
                     ids])
        chats.sort(key=lambda x: x[0], reverse=True)
    opponent = db_sess.query(User).filter(User.id == id).first()
    return render_template('chat.html', messages=messages[::-1], product=product, url=current_url,
                           form=form, chats=chats, opponent=opponent)


@application.route('/personal_account/<int:id>')
def personal_account(id):
    db_sess = db_session.create_session()
    profile = db_sess.query(User).filter(User.id == id).first()
    return render_template('personal_account.html', profile=profile)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


'''******'''


@application.route('/upload_photo', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = request.files['file']
        db_sess = db_session.create_session()
        if f:
            f.save(os.path.join(application.config['UPLOAD_FOLDER'], f'icon-{current_user.id}.png'))
            profile = db_sess.query(User).filter(User.id == current_user.id, current_user.id == User.id).first()
            profile.user_icon = f'icon-{current_user.id}.png'
            db_sess.commit()
            return redirect(f"/personal_account/{current_user.id}")
    return render_template('edit_avatar.html', form=form)


'''******
@application.route('/search/<str:game>')
def search():
    db_sess = db_session.create_session()
    profile = db_sess.query(Games).filter(Games.game_name == name).first()
    return render_template('personal_account.html', profile=profile)'''




@application.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    form = AddGameForm()
    if form.validate_on_submit():
        game_name = form.game_name.data
        file = request.files['file']
        game_name = game_name.replace(' ', '')
        file.save(os.path.join(application.config['UPLOAD_FOLDER1'], f'{game_name}.png'))
        game = Games()
        game.game_name = game_name
        db_sess = db_session.create_session()
        db_sess.add(game)
        db_sess.commit()
        return redirect("/store")
    return render_template('add_game.html', form=form)


@application.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game_name = form.game_name.data
        file = request.files['file']
        ads = Ads()
        ads.id_user = current_user.id
        game = db_sess.query(Games).filter(Games.game_name == form.game_name.data).first()
        ads.id_game = game.id
        ads.name = form.name.data
        ads.description = form.description.data
        ads.product_quantity = form.product_quantity.data
        ads.price = form.price.data
        if file:
            filename = \
                f'{form.price.data}{form.product_quantity.data}{len(form.name.data)}{current_user.id}{game.id}.png'
            file.save(os.path.join(application.config['UPLOAD_FOLDER2'], filename))
            ads.product_photo = filename
        db_sess.add(ads)
        db_sess.commit()
        return redirect("/store")
    return render_template('product-placement.html', form=form)


@application.route('/add_balance/<int:id>', methods=['GET', 'POST'])
@login_required
def add_balance(id):
    form = AddBalanceForm()
    db_sess = db_session.create_session()
    profile = db_sess.query(User).filter(User.id == id).first()
    if form.validate_on_submit():
        amount = form.amount.data
        profile.balance += amount
        db_sess.commit()
        return redirect(f"/personal_account/{id}")
    return render_template('add_balance.html', profile=profile, form=form)


@application.route('/buy/<int:id>', methods=['GET', 'POST'])
@login_required
def buy(id):
    form = ProQForm()
    db_sess = db_session.create_session()
    ads = db_sess.query(Ads).filter(Ads.id == id).first()
    if form.validate_on_submit() and form.amount.data < 1:
        print(11)
        return render_template('buy.html', ads=ads, form=form, message='')
    if form.validate_on_submit() and form.amount.data > ads.product_quantity:
        print(22)
        return render_template('buy.html', ads=ads, form=form, message='')
    if form.validate_on_submit():
        count = form.amount.data
        product = db_sess.query(Ads).options(joinedload(Ads.user)).filter(Ads.id == id).first()
        user = db_sess.query(User).filter(Ads.id == current_user.id).first()
        print(current_user.balance, product.user.balance, product.price * count)
        if current_user.balance > product.price * count:
            user.balance -= product.price * count
            db_sess.commit()
            product.user.balance += product.price * count
            db_sess.commit()
            product.product_quantity -= count
            db_sess.commit()
            return redirect(f"/product/{id}")
    return render_template('buy.html', ads=ads, form=form)


@application.route('/about_us')
def about_us():
    return render_template('about_us.html')

@application.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')


@application.route('/delete_product/<int:id>')
def delete_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Ads).get(id)
    db_sess.delete(product)
    db_sess.commit()
    return redirect("/store")

if __name__ == '__main__':
    application.register_blueprint(ads_api.blueprint)
    application.run(port=5000, host='127.0.0.1')
    serve(application, port=5000, host='0.0.0.0')
