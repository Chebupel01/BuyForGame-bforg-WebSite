from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class AddGameForm(FlaskForm):
    game_name = StringField('Название игры', validators=[DataRequired()])
    submit = SubmitField('')