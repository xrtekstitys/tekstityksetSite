import flask
from flask import make_response, render_template, redirect, request, Blueprint
import nextcloud_client
from api import MatrixHttpApi
from functools import partial
from matrix_actions import matrix
cloud_adress = "" #TODO add this to config

import pickle
import hashlib
id = Blueprint('id', __name__)
id_route = partial(id.route, host="")
def hash_cat(cat):
    hashlib.md5(bytes(cat, 'utf-8')).hexdigest()
    return cat
import pyotp
def get_passwords():
    f = open("secrets.pickle", "rb")
    passwords = pickle.load(f)
    f.close()
    return passwords
def first_time():
    f = open("secrets.pickle", "wb")
    dict1 = {}
    pickle.dump(dict1, f)
    f.close()
def put_user(username, password):
    passwords = get_passwords()
    passwords[username] = password
    f = open("secrets.pickle", "wb")
    pickle.dump(passwords, f)
    f.close()
def set_password(username, password):
    passwords = get_passwords()
    passwords[username] = password
    f = open("secrets.pickle", "wb")
    pickle.dump(passwords, f)
    f.close()
def get_works():
    f = open("works.txt", "r")
    data = f.read()
    f.close()
    data = data.split(";")
    return data
f = open("ft.txt", "r")
if f.read() == "NO":
    first_time()
f.close()
@id_route("/login/")
def login():
    return render_template("login.html")
@id_route("/login/", methods=["POST"])
def post_login():
    username = request.form.get("username")
    password = request.form.get("password")
    passwords = get_passwords()
    resp = make_response(redirect("/"))
    if passwords[username] == hash_cat(password):
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
    cat = make_response(render_template("verification.html"))
    cat.set_cookie("pass", passw)
    cat.set_cookie("username", flask.request.form.get("loginname"))
    return cat
@id_route("/basic_auth/", methods=["GET", "POST"])
def basic_auth():
    if request.method == "GET":
        #print(request.__dict__)
        if "Authorization" in request.headers:
            print(request.headers["Authorization"])
            auth = request.headers["Authorization"]
            auth = auth.replace("Basic ", "")
            auth = auth.split(":")
            username = auth[0]
            password = auth[1]
            passwords = get_passwords()
            if passwords[username] == hash_cat(password):
                resp = make_response("", 200)
            else:
                resp = make_response("", 403)
        
            resp.headers['www-authenticate'] = 'True'
            return resp
        else:
            resp = make_response("", 400)
            resp.headers['www-authenticate'] = 'True'
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
        put_user(username, hash_cat(request.cookies.get("pass")))
        resp = make_response(redirect(cloud_adress))
        resp.delete_cookie('pass')
        resp.delete_cookie('username')
        return resp
    else:
        return "ERORR"
matrix_account = MatrixHttpApi("", token="")
def create_room(element):
    room = MatrixHttpApi.create_room(matrix_account, False, [element])
    room_id = str(room).replace("{'room_id': '", "")
    room_id = str(room_id).replace("'}", "")
    print(room)
    return room_id
def send_verification_message(room_id, element):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    totp = totp.now()
    f = open(f"{element}_otp.txt", "w")
    f.write(totp)
    f.close()
    send_message(room_id, f"")
def send_message(room_id, message):
    MatrixHttpApi.send_message(matrix_account, room_id, message)
    return "OK"
@id_route("/signup/")
def signup_id():
	return render_template("signup.html")
@id_route("/signup-1/")
def signup_id1():
	return render_template("signup-1.html")
@id_route("/signup-1/", methods=["POST"])
def signup_send1():
	username = request.form.get("username")
	password = request.form.get("password")
	matrix.create_user(request)
	return f"User {username} created with password {password}, chat.xrtekstitys.fi"
