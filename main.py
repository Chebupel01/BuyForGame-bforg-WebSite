import os

import requests
from sqlalchemy.orm import joinedload
from waitress import serve
import datetime
from flask_restful import Api
from data.ads import Ads
from data.games import Games
from data.message_form import MesForm
from data.users import User
from data.login_form import LoginForm
from data.reg_form import RegForm
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, current_user
from data import db_session
from data import ads_api
from sqlalchemy import asc, desc
from data import user_api as users_resource

application = Flask(__name__)
application.config['SECRET_KEY'] = 'bforg-site_secret_key'
UPLOAD_FOLDER = 'static/images/users-icons'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    text_for_home = '''Тут кароче будет текст для только что зашедших пользователей'''
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
    db_sess = db_session.create_session()
    product = db_sess.query(Ads).filter(Ads.id == id).first()
    message = form.message.data
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
                           form=form)


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
            print(messages1)
            if messages1:
                chats.append(
                    [datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d %B %Y %H:%M"), user,
                     messages1[-1].split(':', 2)[-1], int(messages1[-1].split(':', 2)[1]),
                     ids])
        chats.sort(key=lambda x: x[0], reverse=True)
    return render_template('chat.html', messages=messages[::-1], product=product, url=current_url,
                           form=form, chats=chats)


@application.route('/personal_account')
def personal_account():
    db_sess = db_session.create_session()
    profile = db_sess.query(User).filter(User.id == id).first()
    return render_template('personal_account.html', profile=profile)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

'''******'''
@application.route('/upload_photo/<int:id>')
def upload(id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f'icon-{id}.png'))
    profile = db_sess.query(User).filter(User.id == id, current_user.id == User.id).first()
    if profile['user-icon'] == 'default-icon.png':
        profile['user-icon'] = f'icon-{id}.png'
        db_sess.commit()


'''******
@application.route('/search/<str:game>')
def search():
    db_sess = db_session.create_session()
    profile = db_sess.query(Games).filter(Games.game_name == name).first()
    return render_template('personal_account.html', profile=profile)'''

@application.route('/about_us')
def about():
    text = '''Приветствую всех тех кто зашел прочесть это сообщение!
Мы писали эту программу своей кровью и потом.
Но чаще чем это играли в доту,
поэтому сайт не прям пушка,
но я считаю что не плохой для своего первого сайта.
А вообще мы с васей ленивые ишаки.
p.s. Человек на фото это михал николаич, который сам попросился в программу'''
    return render_template('about.html', text=text)

if __name__ == '__main__':
    application.register_blueprint(ads_api.blueprint)
    application.run(port=5000, host='127.0.0.1')
    serve(application, port=5000, host='0.0.0.0')
