import flask
from data import db_session
from flask import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
@app.route("/")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def succes():
    if True:  # TODO login
        return redirect("/home")
    return render_template('personal.html', title='Личный Кабинет')


@app.route("/home")
def home():
    global radio_list
    print(radio_list)
    if len(radio_list) == 0:
        return render_template("home_page.html", error=1)
    return render_template("audio_element.html", radio_list=radio_list, error=0)


@app.route('/base')
def base():
    return render_template("base.html")


if __name__ == '__main__':

    radio_list = []
    try:
        with open("radiolist.txt") as file:
            for line in file.readlines():
                radio = line.rstrip("\n").split(",")
                radio_list.append(dict())
                radio_list[-1]["name"] = radio[0]
                radio_list[-1]["link"] = radio[1]
    except Exception as e:
        print("error", e)
    print(radio_list)

    db_session.global_init("db/database.sqlight")

    app.run(port=8080, host="127.0.0.1")
