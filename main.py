from flask import Flask, render_template, redirect

from data.reg_form import RegForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bforg-site_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    form = RegForm()
    if form.validate_on_submit():
        return redirect('/login')
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
