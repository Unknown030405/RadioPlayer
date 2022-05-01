import flask
from data import db_session
from flask import *

from data.all_models.User import User
from forms.LoginForm import LoginForm
from forms.RegistrationForm import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.secret_key = open("file.txt", "rb").readline()

REGISTER_DATA = {"other_href": "http://127.0.0.1:8080/login",
                 "name": "Login"}
LOGIN_DATA = {"other_href": "http://127.0.0.1:8080/register",
              "name": "Registration"}

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
    return res


def check_data(data: dict):
    print(data)
    if not data.get("username", False) or not data.get("password", False):
        return False
    sess = db_session.create_session()
    user = sess.query(User).filter(User.name == data["username"]).first()
    if not user:
        return False
    print(user, user.hashed_password, generate_hash(data["password"]), generate_hash(data["password"]))
    return user.hashed_password == str(generate_hash(data["password"]))


@app.route('/login', methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("entered")

    if form.validate_on_submit():
        print("true")
        if check_data(form.data):
            print("data")
            return redirect(f'/success/{form.data["username"]}')
        print(form.data, session["logined"], sep="\n")
        return render_template('form.html', title='Авторизация', form=form, data=LOGIN_DATA,
                               error_msg="Invalid username or password")
    return render_template('form.html', title='Авторизация', form=form, data=LOGIN_DATA)


def add_user(data: dict):
    user = User()
    if not data.get("username", False) or not data.get("password", False):
        return False
    user.name = data["username"]
    user.hashed_password = generate_hash(data["password"])
    user.email = data.get("email", None)
    sess = db_session.create_session()
    sess.add(user)
    sess.commit()
    return Truegenerate_hash


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if add_user(form.data):
            return redirect(f"/success/{form.data['username']}")
        return render_template("form.html", title="Регистрация", form=form, data=REGISTER_DATA)

    return render_template("form.html", title="Регистрация", form=form, data=REGISTER_DATA)


@app.route('/success/<username>')
def success(username):
    if not username:
        abort(404)
    user = db_session.create_session().query(User).filter(User.name == username).first()
    if not user:
        abort(505)
    logined = session.get("logined", None)
    if not logined:
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
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == session.get("logined", None)).first()

    if request.method == "POST":
        for i in radio_list:
            if request.form.get(i["name"].split()[0], False):
                if user:
                    if i["index"] not in user.followed:
                        user.followed.append(i["index"])
                    else:
                        user.followed.remove(i["index"])
                    sess.add(user)
                    sess.commit()
                    break
                else:
                    logout()

    res_list = list()
    for i in radio_list:
        if i["index"] in user.followed:
            res_list.append(i)
    if not user:
        logout()
    if len(res_list) == 0:
        return render_template("home_page.html", error=1, data={"site": "favorite"}, error_msg="You don't have any favorite radios")
    return render_template("audio_element.html", title="Radio Player Favorites", radio_list=res_list, error=0,
                           user=(user.name if user else ""), data={"site": "favorite"})


@app.route("/home", methods=["GET", "POST"])
def home():
    global radio_list
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == session.get("logined", None)).first()
    if not user:
        return redirect("/login")

    if request.method == "POST":
        for i in radio_list:
            if request.form.get(i["name"].split()[0], False):
                if user:
                    if i["index"] not in user.followed:
                        user.followed.append(i["index"])
                    else:
                        user.followed.remove(i["index"])
                    sess.add(user)
                    sess.commit()
                    break
                else:
                    logout()

    if not user:
        logout()
    if len(radio_list) == 0:
        return render_template("home_page.html", data={"site": "favorite"}, error=1)
    for i in radio_list:
        i["followed"] = i["index"] in user.followed
    print(radio_list)
    return render_template("audio_element.html", title="Radio Player Home Page", radio_list=radio_list, error=0,
                           user=(user.name if user else ""), data={"site": "home"})


@app.route('/base')
def base():
    return render_template("base.html")


if __name__ == '__main__':

    radio_list = []  # TODO radiolist
    try:
        with open("radiolist.txt") as file:
            for line in file.readlines():
                radio = line.rstrip("\n").split(",")
                radio_list.append(dict())
                radio_list[-1]["index"] = str(len(radio_list) - 1)
                radio_list[-1]["name"] = radio[0]
                radio_list[-1]["link"] = radio[1]
                radio_list[-1]["followed"] = False
    except Exception as e:
        print("error", e)

    db_session.global_init("db/database.sqlight")

    app.run(port=8080, host="127.0.0.1")
