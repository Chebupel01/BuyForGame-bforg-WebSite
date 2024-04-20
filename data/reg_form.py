from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
