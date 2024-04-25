from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class ProQForm(FlaskForm):
    amount = IntegerField('Количество товара', validators=[DataRequired()])
    submit = SubmitField('')