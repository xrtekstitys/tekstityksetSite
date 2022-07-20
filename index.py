from functools import partial

import pyotp
from flask import (Blueprint, Flask, flash, make_response, redirect,
                   render_template, request)
from werkzeug.utils import secure_filename

from config import config
from data import data, texts
from handler import handle
from matrix_actions import matrix
from nextcloud import nextcloud

MAIN_DOMAIN = config.MAIN_DOMAIN
MAIN1_DOMAIN = config.MAIN1_DOMAIN
SECOND_DOMAIN = config.SECOND_DOMAIN
JOIN_DOMAIN = config.JOIN_DOMAIN
app = Flask(__name__, host_matching=True, static_host=MAIN_DOMAIN)
second = Blueprint('second', __name__)
second_route = partial(second.route, host=SECOND_DOMAIN)
third = Blueprint('third', __name__)
third_route = partial(third.route, host=MAIN1_DOMAIN)
id = Blueprint('id', __name__)
id_route = partial(id.route, host=JOIN_DOMAIN)
@app.route('/<language>', host=MAIN_DOMAIN)
def redirect1(language):
	if 'matrix' in request.cookies:
		return render_template(f'{language}/index.html')
	else:
		languages = ["fi", "en", "se"]
		if language in languages:
			handle.debug(request)
			return render_template(f'{language}/verify_1.html')
		else:
			return render_template("select.html")
@app.route('/', host=MAIN_DOMAIN)
def select_language():
	handle.debug(request)
	return render_template('select.html')
@app.route("/verify/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify(language):
	element = request.form.get("element")
	handle.debug(request)
	room_id = data.pickles(request)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	f = open(f"{element}_otp.txt", "w")
	f.write(totp)
	f.close()
	matrix.send_message(room_id, f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}")
	resp = make_response(render_template(f"{language}/verify.html"))
	resp.set_cookie('matrix1', element)
	return resp
@app.route("/verify_final/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify1(language):
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	handle.debug(request)
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP("QUZX52M74Q2HL5IZVAY76X4IFEDJNUIF")
	if otp == totp:
		handle.debug(request)
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"{language}/index.html"))
		resp.set_cookie('matrix', element)
		datas = f"{request.remote_addr} with element {element} approved reason: right 2fa code"
		handle.extra_debug(datas)
		return resp
	elif otp == tot1.now():
		handle.debug(request)
		return render_template("admin.html")
	else:
		handle.debug(request)
		return render_template(f'{language}/verify.html')
@app.route("/<language>", methods=["POST"], host=MAIN_DOMAIN)
def upload(language):
	element = request.cookies.get('matrix1')
	handle.debug(request)
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	element = request.cookies.get('matrix')
	file = request.files['file']
	if element.startswith("@"):
		handle.debug(request)
		filename = secure_filename(file.filename)
		data.save_video(file)
		data.save_video_info(filename, request)
		nextcloud.upload_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		nextcloud.upload_file(f"/videot-infot/{filename}_info.txt", f"{filename}.txt")
		datas = f"{element} video uploaded to nextcloud"
		handle.extra_debug(datas)
		link_info = nextcloud.share_link(f"/videot-infot/{filename}")
		matrix.send_message(config.room_id, texts.new_video(link_info))
		handle.debug(request)
		return render_template(f'{language}/uploaded.html')
	else:
		return 'invalid element username'
@third_route('/<language>')
def redirect1(language):
	if 'matrix' in request.cookies:
		return render_template(f'{language}/index.html')
	else:
		languages = ["fi", "en", "se"]
		if language in languages:
			handle.debug(request)
			return render_template(f'{language}/verify_1.html')
		else:
			return render_template("select.html")
@third_route('/')
def select_language():
	handle.debug(request)
	return render_template('select.html')
@third_route("/verify/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify(language):
	element = request.form.get("element")
	handle.debug(request)
	room_id = data.pickles(request)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	f = open(f"{element}_otp.txt", "w")
	f.write(totp)
	f.close()
	matrix.send_message(room_id, f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}")
	resp = make_response(render_template(f"{language}/verify.html"))
	resp.set_cookie('matrix1', element)
	return resp
@third_route("/verify_final/<language>/", methods=["POST"])
def onetime_verify1(language):
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	handle.debug(request)
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP(config.admin_2fa)
	if otp == totp:
		handle.debug(request)
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"{language}/index.html"))
		resp.set_cookie('matrix', element)
		datas = f"{request.remote_addr} with element {element} approved reason: right 2fa code"
		handle.extra_debug(datas)
		return resp
	elif otp == tot1.now():
		handle.debug(request)
		return render_template("admin.html")
	else:
		handle.debug(request)
		return render_template(f'{language}/verify.html')
@third_route("/<language>", methods=["POST"])
def upload(language):
	element = request.cookies.get('matrix1')
	handle.debug(request)
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	element = request.cookies.get('matrix')
	file = request.files['file']
	if element.startswith("@"):
		handle.debug(request)
		filename = secure_filename(file.filename)
		data.save_video(file)
		data.save_video_info(filename, request)
		nextcloud.upload_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		nextcloud.upload_file(f"/videot-infot/{filename}_info.txt", f"{filename}.txt")
		datas = f"{element} video uploaded to nextcloud"
		handle.extra_debug(datas)
		link_info = nextcloud.share_link(f"/videot-infot/{filename}")
		matrix.send_message(config.room_id, texts.new_video(link_info))
		flash('Video successfully uploaded') 
		handle.debug(request)
		return render_template(f'{language}/uploaded.html')
	else:
		return 'invalid element username'
@second_route('/')
def ilmoittaudu():
	handle.extra_debug(datas)
	datas = f"{request.remote_addr} reguested ilmosite"
	handle.extra_debug(datas)
	return render_template('ilmo.html')
@second_route("/ilmoittaudu/", methods=["POST"])
def ilmo_regi():
	etunimi = request.form.get("firstname")
	sukunimi = request.form.get("lastname")
	puhelin = request.form.get("phonenumber")
	telegram = request.form.get("telegram")
	whatsapp = request.form.get("whatsapp")
	litterointi = request.form.get("litterointi")
	kaantaminen = request.form.get("kaantaminen")
	datas = f"{request.remote_addr} posted following datas to ilmosite\n Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen}"
	handle.extra_debug(datas)
	f = open("ilmot.txt", "a")
	f.write(f"Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen},\n")
	f.close()
	return 'Otamme yhteyttä kun olemme katsoneet ilmoittautumisesi.'
@second_route("/admin/")
def admin_panel():
	datas = f"{request.remote_addr} requested ilmo admin site"
	handle.extra_debug(datas)
	f = open("/root/nettisivu/ilmot.txt", "r")
	cat = f.read()
	f.close()
	cats = cat.split(",")
	return render_template("cat.html", cats = cats)
@second_route("/sisainen/")
def sisainen():
	datas = f"{request.remote_addr} requested internal ilmo site"
	handle.extra_debug(datas)
	return render_template("sisainen.html")
@second_route("/sisainen/", methods=["POST"])
def sisainen_post():
	e_username = request.form.get("username")
	handle.debug(request)
	matrix.invite_user_to_rooms(f"@{e_username}:elokapina.fi")
	return 'thank you'
@id_route("/signup/")
def signup_id():
	return render_template("signup.html")
@id_route("/signup-1/")
def signup_id1():
	return render_template("signup-1.html")
@id_route("/signup/", methods=["POST"])
def signup_send():
	username = request.form.get("username")
	password = request.form.get("password")
	secret = request.form.get("secret")
	if secret == config.create_secret:
		nextcloud.create_user(username, password)
		return f"User {username} created with password {password}, you can now sign in at cloud.xrtekstitys.fi."
	else:
		return f"Secret {secret} was wrong"
@id_route("/signup-1/", methods=["POST"])
def signup_send1():
	username = request.form.get("username")
	password = request.form.get("password")
	matrix.create_user(request)
	return f"User {username} created with password {password}, and chat.xrtekstitys.fi"

app.register_blueprint(second)
app.register_blueprint(third)
app.register_blueprint(id)

if __name__ == '__main__':
    app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=config.ssl)
