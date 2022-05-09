import os
import time
import pickle
from settings import client, nc, room_id
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
from app import app
@app.route('/<language>')
def redirect1(language):
	if 'matrix' in request.cookies:
		return render_template(f'{language}/index.html')
	else:
		if language == "fi":
			return render_template('fi/verify_1.html')
		elif language == "en":
			return render_template('en/verify_1.html')
		elif language == "se":
			return render_template('se/verify_1.html')
	return render_template("select.html")
@app.route("/")
def redi():
	return render_template('select.html')
@app.route("/verify/<language>/", methods=["POST"])
def onetime_verify(language):
	element = request.form.get("element")
	element_hash = hashlib.md5(bytes(element, 'utf-8')).hexdigest()
	matrix_token = ""
	matrix = MatrixHttpApi("https://matrix.elokapina.fi", token=matrix_token)
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
		room1 = str(room).replace("'}", "")
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
@app.route("/verify_final/<language>/", methods=["POST"])
def onetime_verify1(language):	
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP("QUZX52M74Q2HL5IZVAY76X4IFEDJNUIF")
	if otp == totp:
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"{language}/index.html"))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		return render_template("admin.html")
	else:
		return render_template(f'{language}/verify.html')
@app.route("/<language>", methods=["POST"])
def upload(language):
	matrix_token = ""
	matrix_username = ""
	room_id = ""
	client = MatrixClient("https://matrix.elokapina.fi", token=matrix_token, user_id=matrix_username)
	nextcloud_username = ""
	nextcloud_password = ""
	nc = nextcloud_client.Client('https://cloud.tekstitykset.elokapina.fi/')
	nc.login(nextcloud_username, nextcloud_password)
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
		print('upload_video filename: ' + filename)
		nc.put_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
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
		link_info = nc.share_file_with_link(f"/videot-infot/{filename}")
		room = client.join_room(room_id)
		room.send_text(f"Hei, uusi video on litteroitavana, videon linkki on: {link_info.get_link()}.\nRakkautta ja raivoa, tekstitykset-bot.")
		flash('Video successfully uploaded') 
		return render_template(f'{language}/uploaded.html')
@app.route('/display/<filename>')
def display_video(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
@app.route('/guide/<language>')
def display_guide(language):
	if language == "fi":
		return render_template('fi/guide.html')
	elif language == "en":
		return render_template('en/guide.html')
	elif language == "se":
		return render_template('se/guide.html')
@app.route('/tools/<tool>')
def tool(tool):
	if tool == "srt":
		return render_template("tool.html")
	elif tool == "cloud":
		return redirect("https://cloud.tekstitykset.elokapina.fi/")
@app.route('/admin')
def admin():
	return render_template("admin.html")
@app.route('/create')
def admin():
	return render_template("admin.html")
@app.route('/create/', methods=["POST"])
def invite1():
	nc = nextcloud_client.Client('https://cloud.tekstitykset.elokapina.fi/')
	nc.login('', '')
	element = request.form.get("element")
	secret = request.form.get("secret")
	password = request.form.get("password")
	if secret == "":
		username = element
		nc.create_user(element, password)
		return render_template("created.html", kauttis = username, password = password)
	else:
		return 'GO HELL'
@app.route('/admin/invite/', methods=["POST"])
def invite1():
	element = request.form.get("element")
	username = element
	rooms = ["!vGpRusmxhqZHWgeDBx:elokapina.fi","!xHNYRcoggfUUdIDlhb:elokapina.fi","!ARuFTKObdJZTganqhP:elokapina.fi"]
	nc.create_user(element, f"{element}ONluova")
	nc.share_file_with_user("/ohje.docx", element)
	room = client.create_room()
	room.set_room_name(f"@stwg:elokapina.fi")
	room.invite_user(f"@{username}:elokapina.fi")
	room.send_text(f'Hei, {element}, minulla on sinulle tunnukset työryhmän omaan cloudiin joka sijaitsee osoitteessa https://cloud.tekstitykset.elokapina.fi, tunnukset ovat:\nKäyttäjänimi: "{element}" ja salasana: "{element}ONluova"')
	for room in rooms:
		room = client.join_room(room)
		room.invite_user(f"@{username}:elokapina.fi")
if __name__ == "__main__":
    app.run(host='tekstitykset.elokapina.fi',port="443",ssl_context=('cert.pem', 'key.pem'))
