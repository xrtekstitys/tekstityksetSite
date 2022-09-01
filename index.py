from functools import partial
import pyotp
from flask import (Blueprint, Flask, flash, make_response, redirect,
                   render_template, request, abort)
from auth import auth
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
def get_language(request):
	if 'language' in request.cookies:
		language = request.cookies.get("language")
		return language
	else:
		return "EN"
@app.before_request
def before():
	handle.debug(request)
	if huolto:
		return abort(503)
@app.route('/select_language/', methods=["GET", "POST"])
def select_language():
	if request.method == "GET":
		return render_template("all/select.html")
	else:
		resp = make_response(redirect("https://tekstitykset.elokapina.fi/"))
		resp.set_cookie('language', language)
		return resp
@app.route('/', host=MAIN_DOMAIN)
def main():
	if auth.check_auth(request):
		return render_template('all/index.html', language=get_language(request))
	else:
		return render_template('all/verify_1.html', language=get_language(request))
@app.route("/verify/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify():
	element = request.form.get("element")
	room_id = data.pickles(request)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	if element.startswith("@"):
		if element.endswith(":elokapina.fi"):
			f = open(f"{element}_otp.txt", "w")
			f.write(totp)
			f.close()
		elif element.endswith(":matrix.org"):
			f = open(f"{element}_otp.txt", "w")
			f.write(totp)
			f.close()
		else:
			abort(403)
	else:
		abort(500)
	matrix.send_message(room_id, f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}")
	resp = make_response(render_template(f"all/verify.html", language=get_language(request)))
	resp.set_cookie('matrix1', element)
	return resp
@app.route("/verify_final/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify1():
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP(config.admin_2fa)
	if otp == totp:
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"all/index.html", language=get_language(request)))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		return render_template("admin.html")
	else:
		return render_template(f'all/verify.html', language=get_language(request))
@app.route("/", methods=["POST"], host=MAIN_DOMAIN)
def upload():
	element = request.cookies.get('matrix1')
	if 'file' not in request.files:
		flash('No file part')
		return redirect(MAIN_DOMAIN)
	element = request.cookies.get('matrix')
	file = request.files['file']
	if element.startswith("@"):
		filename = secure_filename(file.filename)
		data.save_video(file)
		data.save_video_info(filename, request)
		nextcloud.upload_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		nextcloud.upload_file(f"/videot-infot/{filename}_info.txt", f"{filename}.txt")
		
		link_info = nextcloud.share_link(f"/videot-infot/{filename}")
		matrix.send_message(config.room_id, texts.new_video(link_info))
		return render_template(f'all/uploaded.html', language=get_language(request))
	else:
		return 'invalid element username'
@third_route('/')
def redirect1()):
	if auth.check_auth(request):
		return render_template('all/index.html', language=get_language(request))
	else:
		return render_template('all/verify_1.html', language=get_language(request))
@third_route('/')
def select_language():
	return render_template('select.html')
@third_route("/verify/", methods=["POST"])
def onetime_verify():
	element = request.form.get("element")
	room_id = data.pickles(request)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	if element.startswith("@"):
		if element.endswith(":elokapina.fi"):
			f = open(f"{element}_otp.txt", "w")
			f.write(totp)
			f.close()
		elif element.endswith(":matrix.org"):
			f = open(f"{element}_otp.txt", "w")
			f.write(totp)
			f.close()
		else:
			abort(403)
	else:
		abort(500)
	matrix.send_message(room_id, f"Varmennuskoodisi sivustolle tekstitykset.elokapina.fi on: {totp}")
	resp = make_response(render_template(f"all/verify.html", language=get_language(request)))
	resp.set_cookie('matrix1', element)
	return resp
@third_route("/verify_final/", methods=["POST"])
def onetime_verify1():
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	f = open(f"{element}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP(config.admin_2fa)
	if otp == totp:
		f = open(f"{element}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"all/index.html", language=get_language(request)))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		return render_template("admin.html")
	else:
		return render_template(f'all/verify.html', language=get_language(request))
@third_route("/", methods=["POST"])
def upload():
	element = request.cookies.get('matrix1')
	if 'file' not in request.files:
		flash('No file part')
		return redirect(MAIN_DOMAIN)
	element = request.cookies.get('matrix')
	file = request.files['file']
	if element.startswith("@"):
		filename = secure_filename(file.filename)
		data.save_video(file)
		data.save_video_info(filename, request)
		nextcloud.upload_file(f"/videot-infot/{filename}", f"static/uploads/{filename}")
		nextcloud.upload_file(f"/videot-infot/{filename}_info.txt", f"{filename}.txt")		
		link_info = nextcloud.share_link(f"/videot-infot/{filename}")
		matrix.send_message(config.room_id, texts.new_video(link_info))
		flash('Video successfully uploaded') 
		return render_template(f'all/uploaded.html', language=get_language(request))
	else:
		return 'invalid element username'


app.register_blueprint(second)
app.register_blueprint(third)
app.register_blueprint(id)

if __name__ == '__main__':
    app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=config.ssl)