import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = wtforms.EmailField("Электронная почта", validators=[DataRequired()])
    image = FileField("Аватарка")
    submit = SubmitField('Зарегестрироваться')