from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class MesForm(FlaskForm):
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('')