import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileAllowed, FileField


class ProfileForm(FlaskForm):
    email = wtforms.EmailField("Электронная почта")
    image = FileField("Аватарка")
    submit = SubmitField('Сохранить')