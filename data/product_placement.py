from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    game_name = StringField('Название игры', validators=[DataRequired()])
    name = StringField('Название объявления', validators=[DataRequired()])
    description = StringField('Описание объявления', validators=[DataRequired()])
    product_quantity = IntegerField('Количество товара', validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    submit = SubmitField('')