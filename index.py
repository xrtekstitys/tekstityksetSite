import os
import xml.etree.ElementTree as ET
from app import app
from matrix_client.client import MatrixClient
import nextcloud_client
import urllib.request
import requests
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as moviepy
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
def make_link(duuni1):
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
    return re2
@app.route('/<language>')
def redirect(language):
	if language == "fi":
		return render_template('fi/index.html')
	elif language == "en":
		return render_template('en/index.html')
	elif language == "se":
		return render_template('se/index.html')
@app.route("/")
def redi():
	return render_template('select.html')
@app.route("/<language>", methods=["POST"])
def upload(language):
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	element = request.form.get("element")
	file = request.files['file']
	duuni = request.form.get("duuni")
	englanti = request.form.get("English")
	ruotsi = request.form.get("Sweden")
	if element.startswith("@"):
		element_s = element.split(":")
		if element_s[1] == "elokapina.fi":
			filename = secure_filename(file.filename)
			duuni1 = secure_filename(duuni)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print('upload_video filename: ' + filename)
			client = MatrixClient("https://matrix.elokapina.fi", token="", user_id="")
			nc = nextcloud_client.Client('https://cloud.elokapina.fi/')
			nc.login('', '')
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
			re2 = make_link(duuni1)
			link_info = nc.share_file_with_link(f'{duuni1}.mp4')
			room = client.join_room("!xHNYRcoggfUUdIDlhb:elokapina.fi")
			room.send_text(f"Hei, uusi video on auennut litteroitavaksi, videon voi ladata osoitteesta {link_info.get_link()}, merkkaa {re2} <-- tuonne, element käyttäjätunnuksesi sekä se minkä pätkän litteroit, niin ei tule tuplia.")
			flash('Video successfully uploaded')
			return render_template(f'{language}/uploaded.html')
		else:
			return render_template(f'{language}/permissions.html')
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
