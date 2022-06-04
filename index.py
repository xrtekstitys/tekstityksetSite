from functools import partial
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, Blueprint
from matrix_client.api import MatrixHttpApi
import nextcloud_client
import pickle
import pyotp
import hashlib
import os
import os
import time
import pickle
import urllib.request
import hashlib
import os.path
import xml.etree.ElementTree as ET
import moviepy.editor as moviepy
import nextcloud_client
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
import pyotp
import requests
from flask import Flask, flash, redirect, render_template, request, url_for, make_response
from flask import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from werkzeug.utils import secure_filename
MAIN_DOMAIN = 'tekstitykset.elokapina.fi'
MAIN1_DOMAIN = 'xrtekstitys.fi'
SECOND_DOMAIN = 'ilmo.xrtekstitys.fi'
JOIN_DOMAIN = 'id.xrtekstitys.fi'
app = Flask(__name__, host_matching=True, static_host=MAIN_DOMAIN)
second = Blueprint('second', __name__)
second_route = partial(second.route, host=SECOND_DOMAIN)
third = Blueprint('third', __name__)
third_route = partial(third.route, host=MAIN1_DOMAIN)
id = Blueprint('id', __name__)
id_route = partial(id.route, host=JOIN_DOMAIN)
@app.route('/<language>', host=MAIN_DOMAIN)
def redirect1(language):
	import matrix_debug
	if 'matrix' in request.cookies:
		return render_template(f'{language}/index.html')
	else:
		if language == "fi":
			ip_addr = request.remote_addr
			data = f"{ip_addr} language `FI`"
			matrix_debug.send_debug(data)
			return render_template('fi/verify_1.html')
		elif language == "en":
			ip_addr = request.remote_addr
			data = f"{ip_addr} language `EN`"
			matrix_debug.send_debug(data)
			return render_template('en/verify_1.html')
		elif language == "se":
			ip_addr = request.remote_addr
			data = f"{ip_addr} language `SE`"
			matrix_debug.send_debug(data)
			return render_template('se/verify_1.html')
	return render_template("select.html")
@app.route('/', host=MAIN_DOMAIN)
def select_language():
	return render_template('select.html')
@app.route("/verify/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify(language):
	import matrix_debug
	element = request.form.get("element")
	ip_addr = request.remote_addr
	data = f"{element} from ip {ip_addr} started 2fa verification"
	matrix_debug.send_debug(data)
	element_hash = hashlib.md5(bytes(element, 'utf-8')).hexdigest()
	matrix_token = ""
	matrix = MatrixHttpApi("", token=matrix_token)
	if os.path.exists("./cant.pickle"):
		with open('./cant.pickle', 'br') as file:
			matrix_map = pickle.load(file)
			if element_hash in matrix_map:
				room1 = matrix_map[element_hash]
			else:
				room = MatrixHttpApi.create_room(matrix)
				print(str(room))
				room1 = str(room).replace("{'room_id': '", "")
				room1 = str(room1).replace("'}", "")
				MatrixHttpApi.set_room_name(matrix, room1, "Vahvistuskoodi, tekstitykset.elokapina.fi")
				MatrixHttpApi.invite_user(matrix, room1, element)
				matrix_map[element_hash] = room1
				with open('./cant.pickle', 'bw') as file:
					pickle.dump(matrix_map, file)
	else:
		room = MatrixHttpApi.create_room(matrix)
		print(str(room))
		room1 = str(room).replace("{'room_id': '", "")
		room1 = str(room1).replace("'}", "")
		MatrixHttpApi.set_room_name(matrix, room1, "Vahvistuskoodi, tekstitykset.elokapina.fi")
		MatrixHttpApi.invite_user(matrix, room1, element)
		matrix_map = dict()
		matrix_map[element_hash] = room1
		with open('./cant.pickle', 'bw') as file:
			pickle.dump(matrix_map, file)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	f = open(f"{element}_otp.txt", "w")
	f.write(totp)
	f.close()
	text = f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}"
	MatrixHttpApi.send_message(matrix, room1, text)
	resp = make_response(render_template(f"{language}/verify.html"))
	resp.set_cookie('matrix1', element)
	return resp
@app.route("/verify_final/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify1(language):
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{element} with ip {ip_addr} sented request to verify 2fa with code {otp}"
	matrix_debug.send_debug(data)
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP("")
	if otp == totp:
		data = f"{element} with ip {ip_addr}´s request to verify is accepted with reason: right 2fa code."
		matrix_debug.send_debug(data)
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"{language}/index.html"))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		data = f"{element} with ip {ip_addr}´s request to verify is accepted with reason: right 2fa admin code."
		matrix_debug.send_debug(data)
		return render_template("admin.html")
	else:
		data = f"{element} with ip {ip_addr}´s request to verify is denied with reason: wrong 2fa code."
		matrix_debug.send_debug(data)
		return render_template(f'{language}/verify.html')
@app.route("/<language>", methods=["POST"], host=MAIN_DOMAIN)
def upload(language):
	import matrix_debug
	element = request.cookies.get('matrix1')
	data = f"{element} started uploading video"
	matrix_debug.send_debug(data)
	import nettisivu
	nc = nettisivu.nc
	client = nettisivu.client
	room_id = nettisivu.room_id
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	element = request.cookies.get('matrix')
	file = request.files['file']
	duuni = request.form.get("duuni")
	englanti = request.form.get("English")
	ruotsi = request.form.get("Sweden")
	if element.startswith("@"):
		filename = secure_filename(file.filename)
		duuni1 = secure_filename(duuni)
		file.save(os.path.join("/root/nettisivu/static/uploads/", filename))
		data = f"{element} video uploaded to server"
		matrix_debug.send_debug(data)
		print('upload_video filename: ' + filename)
		nc.put_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		data = f"{element} video uploaded to nc"
		matrix_debug.send_debug(data)
		if englanti == "English":
			englanti = "Halutaan"
		elif englanti == "None":
			englanti = "Ei haluta"
		if ruotsi == "Sweden":
			ruotsi = "Halutaan"
		elif ruotsi == "None":
			ruotsi = "Ei haluta"
		f = open(f"{duuni1}.txt", "w")
		f.write(f"Element:\n{element} \nKäännökset:\nEnglanti:\n{englanti}\nRuotsi:\n{ruotsi}")
		f.close()
		nc.put_file(f"/videot-infot/{duuni1}_info.txt", f"{duuni1}.txt")
		data = f"{element} video uploaded to nextcloud"
		matrix_debug.send_debug(data)
		link_info = nc.share_file_with_link(f"/videot-infot/{filename}")
		room = client.join_room(room_id)
		room.send_text(f"Hei, uusi video on litteroitavana, videon linkki on: {link_info.get_link()}.\nRakkautta ja raivoa, tekstitykset-bot.")
		flash('Video successfully uploaded') 
		data = f"{element} video sended to workers"
		matrix_debug.send_debug(data)
		return render_template(f'{language}/uploaded.html')
	else:
		return 'invalid element username'
@third_route('/<language>')
def redirect1(language):
	import matrix_debug
	if 'matrix' in request.cookies:
		return render_template(f'{language}/index.html')
	else:
		if language == "fi":
			data = "language FI"
			matrix_debug.send_debug(data)
			return render_template('fi/verify_1.html')
		elif language == "en":
			data = "language EN"
			matrix_debug.send_debug(data)
			return render_template('en/verify_1.html')
		elif language == "se":
			data = "language SE"
			matrix_debug.send_debug(data)
			return render_template('se/verify_1.html')
	return render_template("select.html")
@third_route('/static/FUCXEDCAPSLatin-Regular.woff')
def font():
    return redirect('https://tekstitykset.elokapina.fi/static/FUCXEDCAPSLatin-Regular.woff')
    #<link type="text/css" rel="stylesheet" href="{{url_for('static', filename='mystyle.css')}}"/> 
@third_route('/')
def select_language():
	return render_template('select.html')
@third_route("/verify/<language>/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify(language):
	import matrix_debug
	element = request.form.get("element")
	ip_addr = request.remote_addr
	data = f"{element} from ip {ip_addr} started 2fa verification"
	matrix_debug.send_debug(data)
	element_hash = hashlib.md5(bytes(element, 'utf-8')).hexdigest()
	matrix_token = ""
	matrix = MatrixHttpApi("", token=matrix_token)
	if os.path.exists("./cant.pickle"):
		with open('./cant.pickle', 'br') as file:
			matrix_map = pickle.load(file)
			if element_hash in matrix_map:
				room1 = matrix_map[element_hash]
			else:
				room = MatrixHttpApi.create_room(matrix)
				print(str(room))
				room1 = str(room).replace("{'room_id': '", "")
				room1 = str(room1).replace("'}", "")
				MatrixHttpApi.set_room_name(matrix, room1, "Vahvistuskoodi, tekstitykset.elokapina.fi")
				MatrixHttpApi.invite_user(matrix, room1, element)
				matrix_map[element_hash] = room1
				with open('./cant.pickle', 'bw') as file:
					pickle.dump(matrix_map, file)
	else:
		room = MatrixHttpApi.create_room(matrix)
		print(str(room))
		room1 = str(room).replace("{'room_id': '", "")
		room1 = str(room1).replace("'}", "")
		MatrixHttpApi.set_room_name(matrix, room1, "Vahvistuskoodi, tekstitykset.elokapina.fi")
		MatrixHttpApi.invite_user(matrix, room1, element)
		matrix_map = dict()
		matrix_map[element_hash] = room1
		with open('./cant.pickle', 'bw') as file:
			pickle.dump(matrix_map, file)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	f = open(f"{element}_otp.txt", "w")
	f.write(totp)
	f.close()
	text = f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}"
	MatrixHttpApi.send_message(matrix, room1, text)
	resp = make_response(render_template(f"{language}/verify.html"))
	resp.set_cookie('matrix1', element)
	return resp
@third_route("/verify_final/<language>/", methods=["POST"])
def onetime_verify1(language):
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{element} with ip {ip_addr} sented request to verify 2fa with code {otp}"
	matrix_debug.send_debug(data)
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP("")
	if otp == totp:
		data = f"{element} with ip {ip_addr}´s request to verify is accepted with reason: right 2fa code."
		matrix_debug.send_debug(data)
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"{language}/index.html"))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		data = f"{element} with ip {ip_addr}´s request to verify is accepted with reason: right 2fa admin code."
		matrix_debug.send_debug(data)
		return render_template("admin.html")
	else:
		data = f"{element} with ip {ip_addr}´s request to verify is denied with reason: wrong 2fa code."
		matrix_debug.send_debug(data)
		return render_template(f'{language}/verify.html')
@third_route("/<language>", methods=["POST"])
def upload(language):
	import matrix_debug
	element = request.cookies.get('matrix1')
	ip_addr = request.remote_addr
	data = f"{element} with ip {ip_addr} started uploading video"
	matrix_debug.send_debug(data)
	from nettisivu import client, nc, room_id
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	element = request.cookies.get('matrix')
	file = request.files['file']
	duuni = request.form.get("duuni")
	englanti = request.form.get("English")
	ruotsi = request.form.get("Sweden")
	if element.startswith("@"):
		filename = secure_filename(file.filename)
		duuni1 = secure_filename(duuni)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		data = f"{element} video uploaded to server"
		matrix_debug.send_debug(data)
		print('upload_video filename: ' + filename)
		nc.put_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		data = f"{element} video uploaded to nc"
		matrix_debug.send_debug(data)
		if englanti == "English":
			englanti = "Halutaan"
		elif englanti == "None":
			englanti = "Ei haluta"
		if ruotsi == "Sweden":
			ruotsi = "Halutaan"
		elif ruotsi == "None":
			ruotsi = "Ei haluta"
		f = open(f"{duuni1}.txt", "w")
		f.write(f"Element:\n{element} \nKäännökset:\nEnglanti:\n{englanti}\nRuotsi:\n{ruotsi}")
		f.close()
		nc.put_file(f"/videot-infot/{duuni1}_info.txt", f"{duuni1}.txt")
		data = f"{element} video uploaded to nextcloud"
		matrix_debug.send_debug(data)
		link_info = nc.share_file_with_link(f"/videot-infot/{filename}")
		room = client.join_room(room_id)
		room.send_text(f"Hei, uusi video on litteroitavana, videon linkki on: {link_info.get_link()}.\nRakkautta ja raivoa, tekstitykset-bot.")
		flash('Video successfully uploaded') 
		data = f"{element} video sended to workers"
		matrix_debug.send_debug(data)
		return render_template(f'{language}/uploaded.html')
	else:
		return 'invalid element username'
@second_route('/')
def ilmoittaudu():
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{ip_addr} reguested ilmosite"
	matrix_debug.send_debug(data)
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
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{ip_addr} posted following data to ilmosite\n Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen}"
	matrix_debug.send_debug(data)
	f = open("ilmot.txt", "a")
	f.write(f"Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen},\n")
	f.close()
	return 'Otamme yhteyttä kun olemme katsoneet ilmoittautumisesi.'
@second_route("/admin/")
def admin_panel():
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{ip_addr} requested ilmo admin site"
	matrix_debug.send_debug(data)
	f = open("/root/nettisivu/ilmot.txt", "r")
	cat = f.read()
	f.close()
	cats = cat.split(",")
	return render_template("cat.html", cats = cats)
@second_route("/sisainen/")
def sisainen():
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{ip_addr} requested internal ilmo site"
	matrix_debug.send_debug(data)
	return render_template("sisainen.html")
@second_route("/sisainen/", methods=["POST"])
def sisainen_post():
	client = MatrixClient("", token="",
    	user_id="@:elokapina.fi")
	e_username = request.form.get("username")
	username = request.form.get("usernamew")
	password = request.form.get("password")
	nextcloud_username = ""
	nextcloud_password = ""
	nc = nextcloud_client.Client('https://cloud.tekstitykset.elokapina.fi/')
	nc.login(nextcloud_username, nextcloud_password)
	exists = nc.user_exists(username)
	import matrix_debug
	ip_addr = request.remote_addr
	data = f"{ip_addr} posted following data to internal ilmo site:\n element: {e_username}\n username: {username} \n password: {password}"
	matrix_debug.send_debug(data)
	if exists == True:
		data = f"{ip_addr} with username @{e_username}:elokapina.fi exists in cloud with username {username}"
		matrix_debug.send_debug(data)
		rooms = ["!vGpRusmxhqZHWgeDBx:elokapina.fi","!ARuFTKObdJZTganqhP:elokapina.fi", "!aBgSOqEPQMlIjYGURM:elokapina.fi"]
		for room1 in rooms:
			room = client.join_room(room1)
			room.invite_user(f"@{e_username}:elokapina.fi")
	elif exists == False:
		data = f"{ip_addr} with username @{e_username}:elokapina.fi don´t exists in cloud with username {username}"
		matrix_debug.send_debug(data)
		nc.create_user(username, password)
		rooms = ["!vGpRusmxhqZHWgeDBx:elokapina.fi","!ARuFTKObdJZTganqhP:elokapina.fi", "!aBgSOqEPQMlIjYGURM:elokapina.fi"]
		for room1 in rooms:
				room = client.join_room(room1)
				room.invite_user(f"@{e_username}:elokapina.fi")
	return 'thank you'
@id_route("/signup/")
def signup_id():
	return render_template("signup.html")
@id_route("/signup/", methods=["POST"])
def signup_send():
	username = request.form.get("username")
	password = request.form.get("password")
	secret = request.form.get("secret")
	if secret == "":
		nextcloud_username = ""
		nextcloud_password = ""
		nc = nextcloud_client.Client('https://cloud.tekstitykset.elokapina.fi/')
		nc.login(nextcloud_username, nextcloud_password)
		nc.create_user(username, password)
		return f"User {username} created with password {password}"
	else:
		return f"Secret {secret} was wrong"

app.register_blueprint(second)
app.register_blueprint(third)
app.register_blueprint(id)

if __name__ == '__main__':
    r"""
    Add these to hosts (C:\Windows\System32\drivers\etc\hosts) file:
    127.0.0.1       www.first.local
    127.0.0.1       www.second.local
    """
    app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=('/etc/letsencrypt/live/ilmo.xrtekstitys.fi/fullchain.pem', '/etc/letsencrypt/live/ilmo.xrtekstitys.fi/privkey.pem'))
