import os
import time
import pickle
from settings import client, nc, room_id
import urllib.request
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
	matrix_token = ""
	matrix = MatrixHttpApi("https://matrix.elokapina.fi", token=matrix_token)
	if os.path.exists("./cant.pickle"):
		with open('./cant.pickle', 'br') as file:
			matrix_map = pickle.load(file)
			if hash(element) in matrix_map:
				# Avaa dictionaryn paikalliseen tiedostopolkuun
				with open('./cant.pickle', 'br') as file:
					matrix_map = pickle.load(file)
					room1 = matrix_map[hash(element)]
			else:
				room = MatrixHttpApi.create_room(matrix)
				print(str(room))
				room1 = str(room).replace("{'room_id': '", "")
				room1 = str(room1).replace("'}", "")
				MatrixHttpApi.set_room_name(matrix, room1, element)
				MatrixHttpApi.invite_user(matrix, room1, element)
				matrix_map[hash(element)] = room1
				with open('./cant.pickle', 'bw') as file:
					pickle.dump(matrix_map, file)
	else:
		room = MatrixHttpApi.create_room(matrix)
		print(str(room))
		room1 = str(room).replace("{'room_id': '", "")
		room1 = str(room).replace("'}", "")
		MatrixHttpApi.set_room_name(matrix, room1, element)
		MatrixHttpApi.invite_user(matrix, room1, element)
		matrix_map = dict()
		matrix_map[hash(element)] = room1
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
	resp.set_cookie('matrix', element)
	return resp
@app.route("/verify_final/<language>/", methods=["POST"])
def onetime_verify1(language):	
	element = request.cookies.get('matrix')
	otp = request.form.get("totp_send")
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	if otp == totp:
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		return render_template(f'{language}/index.html')
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
	nc = nextcloud_client.Client('https://cloud.elokapina.fi/')
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
		clip = moviepy.VideoFileClip(f"static/uploads/{filename}")
		clip.write_videofile(f"{duuni1}.mp4")
		nc.put_file(f"{duuni1}.mp4", f"{duuni1}.mp4")
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
		nc.put_file(f"{duuni1}_info.txt", f"{duuni1}.txt")
		nc.copy("Ilmo_malli.xlsx", f'ilmo_{duuni1}.xlsx')
		link_info = nc.share_file_with_link(f'{duuni1}.mp4')
		room = client.join_room(room_id)
		url = "https://cloud.elokapina.fi/ocs/v2.php/apps/files_sharing/api/v1/shares"
		payload=f'path=ilmo_{duuni1}.xlsx&shareType=3'
		headers = {
				'OCS-APIRequest': 'true',
				'Authorization': 'Basic dGVrc3RpdHlrc2V0OlRla3N0aXR5a3NldE9WQVRwYXJoYWl0YQ==',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Cookie': 'cookie_test=test; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc8ap6e5iwyr=ffsifjkob3rqr9m7po5lb2urs1; oc_sessionPassphrase=1NYvqCIVcMtskFV625bXbpz8WYlbARkTGs6dnEyvSVonCZ9XVzm7JaFZZmI52VooTPMnI9kkFi76Z8AzYp67tIg7ovLdDqOTtwpgzTBqUlvxWQJro5r%2BbnOrrzYorIap'
				}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		re = response.text
		re = re.split()
		re2 = re[-5]
		re2 = re2.replace("<url>", "")
		re2 = re2.replace("</url>", "")
		re1 = re[9]
		re1 = re1.replace("<id>", "")
		re1 = re1.replace("</id>", "")
		url = f"https://cloud.elokapina.fi/ocs/v2.php/apps/files_sharing/api/v1/shares/{re1}"
		payload='permissions=3'
		headers = {
				'OCS-APIRequest': 'true',
				'Authorization': 'Basic dGVrc3RpdHlrc2V0OlRla3N0aXR5a3NldE9WQVRwYXJoYWl0YQ==',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Cookie': 'cookie_test=test; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc8ap6e5iwyr=ffsifjkob3rqr9m7po5lb2urs1; oc_sessionPassphrase=1NYvqCIVcMtskFV625bXbpz8WYlbARkTGs6dnEyvSVonCZ9XVzm7JaFZZmI52VooTPMnI9kkFi76Z8AzYp67tIg7ovLdDqOTtwpgzTBqUlvxWQJro5r%2BbnOrrzYorIap'
				}
		response = requests.request("PUT", url, headers=headers, data=payload)
		room.send_text(f"Hei, uusi video on litteroitavana, videon linkki on: {link_info.get_link()}, ilmoittautumislinkki: {re2}.\nRakkautta ja raivoa, tekstitykset-bot.")
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
@app.route('/admin')
def admin():
	f = open("duunit.txt", "r")
	duunit = f.read()
	duunit = duunit.split("---")
	works = duunit
	return render_template("admin.html", works = works)
if __name__ == "__main__":
    app.run(host='tekstitykset.elokapina.fi',port="443",ssl_context=('cert.pem', 'key.pem'))
