import flask
from flask import make_response, render_template, redirect, request, Blueprint
import nextcloud_client
import pyotp
from functools import partial
from matrix_actions import matrix
from config import JOIN_DOMAIN, CLOUD_LOCATION, MATRIX_SERVER, MATRIX_TOKEN

cloud_adress = CLOUD_LOCATION

from db import db
import pickle
import hashlib

id = Blueprint("id", __name__)
id_route = partial(id.route, host=JOIN_DOMAIN)


def get_language(request):
    if "language" in request.cookies:
        language = request.cookies.get("language")
        return language
    else:
        return "EN"


def hash_cat(cat):
    hashlib.md5(bytes(cat, "utf-8")).hexdigest()  # TODO #23 Add better encryption
    return cat


def put_user(username, password):
    db.put_user(username, password, f"@{username}:elokapina.fi")


def set_password(username, password):
    db.set_user(username, password)


def is_password_right(username, password):
    userdata = db.get_user(username)
    if userdata[0] == hash_cat(password):
        print(userdata)
        return True
    else:
        print(userdata)
        print(userdata[0])
        return False


def get_works():
    f = open("works.txt", "r")
    data = f.read()
    f.close()
    data = data.split(";")
    return data


@id_route("/login/")
def login():
    return render_template("login.html")


@id_route("/login/", methods=["POST"])
def post_login():
    username = request.form.get("username")
    password = request.form.get("password")
    resp = make_response(redirect("/"))
    if is_password_right(username, password):
        resp.set_cookie("login", username)
    return resp


@id_route("/register/")
def register():
    return render_template("signup.html")


@id_route("/register/", methods=["POST"])
def hook():
    element = flask.request.form.get("loginname")
    id = create_room(element)
    send_verification_message(id, element)
    passw = flask.request.form.get("password")
    cat = make_response(
        render_template("verification.html", language=get_language(request))
    )
    cat.set_cookie("pass", hash_cat(passw))
    cat.set_cookie("username", flask.request.form.get("loginname"))
    return cat


@id_route("/basic_auth/", methods=["GET", "POST"])
def basic_auth():
    if request.method == "GET":
        # print(request.__dict__)
        if "Authorization" in request.headers:
            print(request.headers["Authorization"])
            auth = request.headers["Authorization"]
            auth = auth.replace("Basic ", "")
            auth = auth.split(":")
            username = auth[0]
            password = auth[1]
            if is_password_right(username, password):
                resp = make_response("", 200)
            else:
                resp = make_response("", 403)

            resp.headers["www-authenticate"] = "True"
            return resp
        else:
            resp = make_response("", 400)
            resp.headers["www-authenticate"] = "True"
            return resp
    else:
        print(request.__dict__)
        print(request.form)
        return "cat", 200


@id_route("/")
def index():
    if request.cookies["login"] and not request.cookies.get("login") == "":
        works = get_works()
        return render_template("sisa/index.html", works=works)
    else:
        return render_template("login.html")


@id_route("/ohjeet/")
def ohje():
    return render_template("ohjeet.html")


@id_route("/verification/", methods=["POST"])
def verification():
    username = flask.request.cookies.get("username")
    code = flask.request.form.get("code")
    f = open(f"{username}_otp.txt", "r")
    data = f.read()
    f.close()
    username = username.replace("@", "")
    username = username.replace(":elokapina.fi", "")
    if code == data:
        put_user(username, request.cookies.get("pass"))
        resp = make_response(redirect(cloud_adress))
        resp.delete_cookie("pass")
        resp.delete_cookie("username")
        return resp
    else:
        return "ERORR"


def create_room(element):

    return matrix.create_room(element)


def send_verification_message(room_id, element):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    totp = totp.now()
    f = open(f"{element}_otp.txt", "w")
    f.write(totp)
    f.close()
    send_message(room_id, f"")


def send_message(room_id, message):
    matrix.send_message(room_id, message)
    return "OK"


@id_route("/signup/")
def signup_id():
    return render_template("signup.html", language=get_language(request))
