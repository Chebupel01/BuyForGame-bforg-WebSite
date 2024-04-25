from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class AddBalanceForm(FlaskForm):
    amount = IntegerField('Внести', validators=[DataRequired()])
    submit = SubmitField('')