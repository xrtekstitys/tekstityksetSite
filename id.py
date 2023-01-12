from otp import is_otp_right, create_otp
import hashlib
import db
import flask
from flask import make_response, render_template, redirect, request, Blueprint, abort
from functools import partial
from matrix_actions import matrix
from config import JOIN_DOMAIN, CLOUD_LOCATION

cloud_adress = CLOUD_LOCATION

id = Blueprint("id", __name__)
id_route = partial(id.route, host=JOIN_DOMAIN)


def get_language(request):
    if "language" in request.cookies:
        language = request.cookies.get("language")
        return language
    else:
        return "EN"


def hash_cat(cat):
    # TODO #23 Add better encryption
    hashlib.md5(bytes(cat, "utf-8")).hexdigest()
    return cat


def put_user(username, password):
    db.put_user(username, password, f"@{username}:elokapina.fi")


def set_password(username, password):
    db.set_user(username, password)


def is_password_right(username, password):
    userdata = db.get_user(username)
    if userdata[0] == hash_cat(password):
        return True
    else:
        return False


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
    response = make_response(
        render_template("verification.html", language=get_language(request))
    )
    response.set_cookie("pass", hash_cat(passw))
    response.set_cookie("username", flask.request.form.get("loginname"))
    return response


@id_route("/basic_auth/", methods=["GET", "POST"])
def basic_auth():
    if request.method == "GET":
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


@id_route("/verification/", methods=["POST"])
def verification():
    username = flask.request.cookies.get("username")
    code = flask.request.form.get("code")
    username = username.replace("@", "")
    username = username.replace(":elokapina.fi", "")
    if is_otp_right(username, code):
        put_user(username, request.cookies.get("pass"))
        resp = make_response(redirect(cloud_adress))
        resp.delete_cookie("pass")
        resp.delete_cookie("username")
        return resp
    else:
        abort(500)


def create_room(element):

    return matrix.create_room(element)


def send_verification_message(room_id, element):
    totp = create_otp(element)
    send_message(room_id, f"Your 2fa code is {totp}")


def send_message(room_id, message):
    matrix.send_message(room_id, message)
    return "OK"


@id_route("/signup/")
def signup_id():
    return render_template("signup.html", language=get_language(request))
