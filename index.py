from functools import partial

import pyotp
from flask import (Blueprint, Flask, flash, make_response, redirect,
                   render_template, request, abort)
from werkzeug.utils import secure_filename
from id import id_route, id
from config import config
from data import data, texts
from handler import handle
from matrix_actions import matrix
from nextcloud import nextcloud
from second import second
huolto = False
MAIN_DOMAIN = config.MAIN_DOMAIN
MAIN1_DOMAIN = config.MAIN1_DOMAIN
app = Flask(__name__, host_matching=True, static_host=MAIN_DOMAIN)
third = Blueprint('third', __name__)
third_route = partial(third.route, host=MAIN1_DOMAIN)

@app.before_request
def before():
	if huolto:
		return abort(503)
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
	alskdlksad = ""
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
@app.route("/<language>", methods=["POST"], host=MAIN_DOMAIN)
def upload(language):
	element = request.cookies.get('matrix1')
	handle.debug(request)
	if 'file' not in request.files:
		flash('No file part')
		return redirect(MAIN_DOMAIN)
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
@third_route("/verify/<language>/", methods=["POST"], host=MAIN1_DOMAIN)
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
		return redirect(MAIN_DOMAIN)
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


app.register_blueprint(second)
app.register_blueprint(third)
app.register_blueprint(id)

if __name__ == '__main__':
    app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=config.ssl)
