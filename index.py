from functools import partial
import pyotp
from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    abort,
)
from auth import auth
from werkzeug.utils import secure_filename
from transfer_data import transfer
from config import (
    ROOM_ID,
    MAIN_DOMAIN,
    MAIN1_DOMAIN
)
from data import data, texts, get_room_id

from matrix_actions import matrix
from nextcloud import nextcloud

from otp import create_otp, is_otp_right

app1 = Blueprint("app1", __name__)
app2 = Blueprint("app2", __name__)


def securate(thing):
    return secure_filename(thing)


def get_language(request):
    if "language" in request.cookies:
        language = request.cookies.get("language")
        return language
    else:
        return redirect("/select_language/")


@app1.route("/select_language/", methods=["GET", "POST"], host=MAIN1_DOMAIN)
@app2.route("/select_language/", methods=["GET", "POST"], host=MAIN_DOMAIN)
def select_language():
    if request.method == "GET":
        return render_template("all/select.html")  # Render all/select.html
    else:  # If request is not HTTP GET
        resp = make_response(
            redirect(request.host)
        )  # Uudelleen ohjaa pyynnön domainiin
        resp.set_cookie("language", language)
        return resp


@app1.route("/", host=MAIN1_DOMAIN)
@app2.route("/", host=MAIN_DOMAIN)
def main():
    # Jos käyttäjä on jo varmennettu aiemmin, ohjaa suoraan videon lataamiseen
    if auth.check_auth(request):
        return render_template("all/index.html", language=get_language(request))
    else:
        return render_template("all/verify_1.html", language=get_language(request))


@app1.route("/", methods=["POST"], host=MAIN1_DOMAIN)
@app2.route("/", methods=["POST"], host=MAIN_DOMAIN)
def upload():
    element = request.cookies.get("matrix1")
    if "file" not in request.files:  # Jos ei tiedostoja
        flash("No file part")
        return redirect(MAIN_DOMAIN)
    element = request.cookies.get("matrix")
    file = request.files["file"]
    if element.startswith("@"):  # Validate username
        filename = secure_filename(file.filename)
        data.save_video(file)
        data.save_video_info(filename, request)
        nextcloud.upload_file(
            f"/videot-infot/{filename}", f"static/uploads/{filename}")
        nextcloud.upload_file(
            f"/videot-infot/{filename}_info.txt", f"{filename}.txt")
        link_info = nextcloud.share_link(f"/videot-infot/{filename}")
        matrix.send_message(ROOM_ID, texts.new_video(link_info))
        return render_template(f"all/uploaded.html", language=get_language(request))
    else:  # If validating of username fails
        return "invalid element username"


@app1.route("/verify/", methods=["POST"], host=MAIN1_DOMAIN)
@app2.route("/verify/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify():
    element = request.form.get("element")
    room_id = get_room_id(element)
    if element.startswith("@"):
        totp = create_otp(element)
    else:
        abort(500)
    matrix.send_message(
        room_id, f"Varmennuskoodisi sivustolle {request.host} on: {totp}"
    )
    resp = make_response(
        render_template(f"all/verify.html", language=get_language(request))
    )
    resp.set_cookie("matrix1", element)
    return resp


@app1.route("/verify_final/", methods=["POST"], host=MAIN1_DOMAIN)
@app2.route("/verify_final/", methods=["POST"], host=MAIN_DOMAIN)
def onetime_verify1():
    element = request.cookies.get("matrix1")
    otp = request.form.get("totp_send")
    if is_otp_right(element, otp):
        resp = make_response(
            render_template(f"all/index.html", language=get_language(request))
        )
        resp.set_cookie("matrix", element)
        return resp
    else:
        return render_template(f"all/verify.html", language=get_language(request))
