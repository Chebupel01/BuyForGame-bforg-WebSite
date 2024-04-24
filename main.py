from waitress import serve
from flask_restful import Api
from data.ads import Ads
from data.games import Games
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


@application.route('/store')
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


@application.route('/product/<int:id>')
def product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Ads).filter(Ads.id == id).first()
    return render_template('product.html', product=product)


"""@app.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <img src="static/img/photo.png" class="img-thumbnail" alt=''>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'photo.png'))
        return "Форма отправлена"""

"""@application.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <img src="static/img/photo.png" class="img-thumbnail" alt=''>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'photo.png'))
        return "Форма отправлена"""

'''******'''
@application.route('/personal_account')
@login_required
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


'''******'''
@application.route('/search/<str:game>')
def search():
    db_sess = db_session.create_session()
    profile = db_sess.query(Games).filter(Games.game_name == name).first()
    return render_template('personal_account.html', profile=profile)

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
