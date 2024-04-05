from data.users import User
from data.login_form import LoginForm
from data.reg_form import RegForm
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_manager, login_user, logout_user, login_required, current_user
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/db_ads.db')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
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
        user.age = form.age.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.set_password(user.hashed_password)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Зарегистрироваться',
                           form=form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
