from functools import partial
import pyotp
from flask import (Blueprint, Flask, flash, make_response, redirect,
                   render_template, request, abort)
from auth import auth
from werkzeug.utils import secure_filename
from id import id_route, id
from transfer_data import transfer
from config import config
from data import data, texts
from handler import handle
from matrix_actions import matrix
from nextcloud import nextcloud
from second import second
if config.testmode_true == True:
	MAIN_DOMAIN = config.TEST_MAIN_DOMAIN
	MAIN1_DOMAIN = config.TEST_MAIN1_DOMAIN
else:
	MAIN_DOMAIN = config.MAIN_DOMAIN
	MAIN1_DOMAIN = config.MAIN1_DOMAIN
app = Flask(__name__, host_matching=True, static_host=MAIN_DOMAIN)
app1 = Blueprint('app1', __name__)
def securate(thing):
	return secure_filename(thing)
def get_language(request):
	if 'language' in request.cookies:
		language = request.cookies.get("language")
		return language
	else:
		return "EN"
@app.before_first_request
def before_first_request():
	response = requests.get("https://uptimerobot.com/inc/files/ips/IPv4.txt")
	uptimerobot_ips = response.content
	app.logger.debug('Initializin uptimerobot ips')
@app.before_request # Suoritetaan aina ennen pyyntöön vastaamista
def before():
	handle.debug(request)
	if config.testmode_true == True or config.maintanence_true == True:
		if request.remote_addr in uptimerobot_ips or request.remote_addr in config.testmode_ips or request.remote_addr in config.maintanence_ips:
			app.logger.info("Letted user in, because user is from us or uptimerobot")
		else:
			abort(503)
@app1.route('/select_language/', methods=["GET", "POST"], host=MAIN1_DOMAIN)
@app.route('/select_language/', methods=["GET", "POST"])
def select_language(): # Toiminto on kielen valitsemista varten
	if request.method == "GET": # Jos pyyntö on HTTP GET pyyntö
		return render_template("all/select.html") # Renderöi all/select.html
	else: # Jos pyyntö ei ole HTTP GET pyyntö
		resp = make_response(redirect(request.host)) # Uudelleen ohjaa pyynnön domainiin
		resp.set_cookie('language', language)
		return resp

@app1.route('/', host=MAIN1_DOMAIN)
@app.route('/', host=MAIN_DOMAIN)
def main():
	if auth.check_auth(request): # Jos käyttäjä on jo varmennettu aiemmin, ohjaa suoraan videon lataamiseen
		return render_template('all/index.html', language=get_language(request))
	else:
		return render_template('all/verify_1.html', language=get_language(request))
@app1.route("/", methods=["POST"], host=MAIN1_DOMAIN)
@app.route("/", methods=["POST"], host=MAIN_DOMAIN)
def upload():
	element = request.cookies.get('matrix1')
	if 'file' not in request.files: # Jos ei tiedostoja
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
@app1.route("/verify/", methods=["POST"], host=MAIN1_DOMAIN)
@app.route("/verify/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify():
	element = request.form.get("element")
	room_id = data.pickles(request)
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	totp = totp.now()
	if element.startswith("@"):
		if element.endswith(":elokapina.fi"):
			f = open(f"{securate(element)}_otp.txt", "w")
			f.write(totp)
			f.close()
		elif element.endswith(":matrix.org"):
			f = open(f"{securate(element)}_otp.txt", "w")
			f.write(totp)
			f.close()
		else:
			abort(403)
	else:
		abort(500)
	matrix.send_message(room_id, f"Varmennuskoodisi sivustolle {request.host} on: {totp}")
	resp = make_response(render_template(f"all/verify.html", language=get_language(request)))
	resp.set_cookie('matrix1', element)
	return resp
@app1.route("/verify_final/", methods=["POST"], host=MAIN1_DOMAIN)
@app.route("/verify_final/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify1():
	element = request.cookies.get('matrix1')
	otp = request.form.get("totp_send")
	f = open(f"{securate(element)}_otp.txt", "r")
	totp = f.read()
	f.close()
	tot1 = pyotp.TOTP(config.admin_2fa)
	if otp == totp:
		f = open(f"{securate(element)}_otp.txt", "w")
		f.write("")
		f.close()
		resp = make_response(render_template(f"all/index.html", language=get_language(request)))
		resp.set_cookie('matrix', element)
		return resp
	elif otp == tot1.now():
		return render_template("admin.html")
	else:
		return render_template(f'all/verify.html', language=get_language(request))
app.register_blueprint(second)
app.register_blueprint(third)
app.register_blueprint(id)

if __name__ == '__main__':
	if config.testmode_true == True:
    	app.run(host=TEST_MAIN_DOMAIN, port=443, debug=True, threaded=True,ssl_context=config.ssl)
	else:
		app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=config.ssl)
