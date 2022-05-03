import os

import wtforms

from data import db_session
from flask import *
from werkzeug.utils import secure_filename
from data.all_models.User import User
from data.all_models.Radio import Radio
from forms.LoginForm import LoginForm
from forms.RegistrationForm import RegistrationForm
from forms.ProfileForm import ProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.secret_key = open("file.txt", "rb").readline()

GLOBAL_SESSION = None

REGISTER_DATA = {"other_href": "http://127.0.0.1:8080/login",
                 "name": "Login"}
LOGIN_DATA = {"other_href": "http://127.0.0.1:8080/register",
              "name": "Registration"}
PROFILE_DATA = {"site": "profile", "constants": [
    {"name": "Имя",
     "value": None}
]}

PRIME = 1523807
MOD = 1000000000000000007


def generate_hash(string):
    step = PRIME
    res = 1
    for i in string:
        res *= step * ord(i)
        res %= MOD
        step *= PRIME
        res %= MOD
    return str(res)


def check_data(data: dict):
    print(data)
    if not data.get("username", False) or not data.get("password", False):
        return False
    user = get_user(name=data["username"])
    if not user:
        return False
    if user.hashed_password == str(generate_hash(data["password"])):
        session["stay_logged"] = data.get("remember_me", False)
        return True
    return False


@app.route('/login', methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("entered")
    user = get_user(id=session["logined"])
    if user:
        return success(user.name)

    if form.validate_on_submit():
        print("true")
        if check_data(form.data):
            print("data")
            return success(form.data["username"])
        print(form.data, session.get("logined"), sep="\n")
        return render_template('form.html', title='Авторизация', form=form, data=LOGIN_DATA,
                               error_msg="Invalid username or password")
    return render_template('form.html', title='Авторизация', form=form, data=LOGIN_DATA)


def add_user(data: dict, form=None):
    user = User()
    if not data.get("username", False) or not data.get("password", False):
        return False
    user.name = data["username"]
    user.hashed_password = str(generate_hash(data["password"]))
    user.email = data.get("email", None)
    if data.get("image"):
        img = form.image.data
        filename = secure_filename(img.filename)
        print(filename)
        if filename == "default.jpg":
            filename = "default(1).jpg"
        path = os.path.join("static", "user_photo", filename)
        img.save(path)
        user.image = filename

    sess = GLOBAL_SESSION
    sess.add(user)
    sess.commit()
    return True


def change_user(ident, form):
    data = form.data
    sess = GLOBAL_SESSION
    user = sess.query(User).filter(User.id == ident).first()
    print(data, form.image, form.image.data, sep="\n")
    if data.get("image", False):
        img = form.image.data
        filename = secure_filename(img.filename)
        print(filename)
        if filename == "default.jpg":
            filename = "default(1).jpg"
        path = os.path.join("static", "user_photo", filename)
        img.save(path)
        user.image = filename
    if data.get("email", False):
        user.email = data["email"]
    if not user.image:
        user.image = "default.jpg"
    sess.commit()
    return True


def get_user(name=None, id=None) -> User:
    sess = GLOBAL_SESSION
    user = None
    if name:
        user = sess.query(User).filter(User.name == name).first()
    if id:
        user = sess.query(User).filter(User.id == id).first()
    return user


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if add_user(form.data, form):
            return success(form.data['username'])
        return render_template("form.html", title="Регистрация", form=form, data=REGISTER_DATA)

    return render_template("form.html", title="Регистрация", form=form, data=REGISTER_DATA)


def add_radio(name, source):
    radio = Radio()
    radio.name = name
    radio.source = source
    db_sess = GLOBAL_SESSION
    db_sess.add(radio)
    db_sess.commit()


def delete_radio(id=None):
    db_sess = GLOBAL_SESSION
    if id:
        db_sess.query(Radio).filter(Radio.id == id).delete()
    db_sess.commit()


def find_radio_by_name(id):
    db_sess = GLOBAL_SESSION
    radio = db_sess.query(Radio).filter(Radio.id == id)[0]
    return radio


def find_radio_by_source(source):
    db_sess = GLOBAL_SESSION
    radio = db_sess.query(Radio).filter(Radio.source == source)[0]
    return radio


def get_all_radios():
    db_sess = GLOBAL_SESSION
    radios = db_sess.query(Radio).all()
    return radios


@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    user = get_user(id=session.get("logined", None))
    if not user:
        return redirect("login")
    PROFILE_DATA["constants"][0]["value"] = user.name
    PROFILE_DATA["path"] = os.path.join("user_photo", user.image)
    print(user.image)
    if form.validate_on_submit():
        ident = session.get("logined")
        if not ident:
            return redirect("/login")
        if change_user(ident, form):
            user = get_user(id=session.get("logined", None))
            PROFILE_DATA["path"] = os.path.join("user_photo", user.image)
            print(user.image, *PROFILE_DATA.items(), sep="\n")
            return render_template("profile_form.html", user=(user.name if user else ""), title="Регистрация",
                                   form=form,
                                   data=PROFILE_DATA, img={(user.image if user else "")}, error=0)
        return render_template("profile_form.html", title="Регистрация", form=form, data=PROFILE_DATA, error=1,
                               error_msg="Cannot commit changes")

    return render_template("profile_form.html", user=(user.name if user else ""), title="Регистрация", form=form,
                           data=PROFILE_DATA, img={(user.image if user else "")}, error=0)


def success(username):
    user = get_user(name=username)
    if not user:
        print(f"Failed to 'success' {username}")
        return redirect("/login")
    logined = session.get("logined", None)
    session["logined"] = user.id
    return make_response(redirect("/home"))


@app.route("/logout")
def logout():
    user = session.get("logined")
    if user:
        session["logined"] = None
    return redirect("/login")


@app.route("/favorite", methods=["GET", "POST"])
def favorite():
    global radio_list
    sess = GLOBAL_SESSION
    user = sess.query(User).filter(User.id == session.get("logined", None)).first()

    if request.method == "POST":
        for i in radio_list:
            if request.form.get(str(i.id), False):
                if user:
                    if i not in user.followed:
                        user.followed.append(i)
                    else:
                        user.followed.remove(i)
                    sess.add(user)
                    sess.commit()
                    break
                else:
                    logout()

    res_list = list()
    for i in radio_list:
        if i in user.followed:
            i.followed = True
            res_list.append(i)
    if not user:
        logout()
    if len(res_list) == 0:
        return render_template("home_page.html", error=1, user=(user.name if user else ""),
                               data={"site": "favorite", 'path': os.path.join("user_photo", user.image)},
                               error_msg="You don't have any favorite radios")
    return render_template("audio_element.html", title="Radio Player Favorites", radio_list=res_list, error=0,
                           user=(user.name if user else ""),
                           data={"site": "favorite", 'path': os.path.join("user_photo", user.image)})


@app.route("/home", methods=["GET", "POST"])
def home():
    print("home")
    global radio_list
    sess = GLOBAL_SESSION
    user = sess.query(User).filter(User.id == session.get("logined", None)).first()
    if not user:
        return redirect("/login")
    print(user.followed)
    if not user.image:
        user.image = "default.jpg"
        sess.commit()

    if request.method == "POST":
        for i in radio_list:
            if request.form.get(str(i.id), False):
                if user:
                    print("....", user.followed)
                    if i not in user.followed:
                        user.followed.append(i)
                    else:
                        user.followed.remove(i)
                    print(user.followed, "---")
                    sess.add(user)
                    sess.commit()
                    break
                else:
                    logout()
    
    if not user:
        return redirect("/login")
    if len(radio_list) == 0:
        return render_template("home_page.html",
                               data={"site": "home", 'path': os.path.join("user_photo", user.image)}, error=1)
    for i in radio_list:
        i.followed = i in user.followed
    return render_template("audio_element.html", title="Radio Player Home Page", radio_list=radio_list, error=0,
                           user=(user.name if user else ""),
                           data={"site": "home", 'path': os.path.join("user_photo", user.image)})


@app.route('/base')
def base():
    return render_template("base.html")


def get_radios_from_csv(filename, splitter):
    file = open(filename)
    headers = file.readline().rstrip('\n').split(splitter)
    for line in file.readlines():
        name, source = line.rstrip("\n").split(splitter)
        add_radio(name, source)


if __name__ == '__main__':

    radio_list = []  # TODO radiolist
    db_session.global_init("db/database.sqlight")
    GLOBAL_SESSION = db_session.create_session()

    try:
        # get_radios_from_csv("radiolist.txt", ",")
        radio_list = get_all_radios()
    except Exception as e:
        print("error", e)
    print(*map(lambda x: [x.name, x.source], radio_list), sep="\n")

    app.run(port=8080, host="127.0.0.1")
