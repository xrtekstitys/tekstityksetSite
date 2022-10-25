from flask import (
    Blueprint,
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    abort,
)
from config import (SECOND_DOMAIN)
from functools import partial
second = Blueprint("second", __name__)
second_route = partial(second.route, host=SECOND_DOMAIN)

@second_route("/admin/")
def admin_panel():
    datas = f"{request.remote_addr} requested ilmo admin site"
    
    f = open("/root/nettisivu/ilmot.txt", "r")
    cat = f.read()
    f.close()
    cats = cat.split(",")
    return render_template("cat.html", cats=cats)


@second_route("/")
def sisainen():
    datas = f"{request.remote_addr} requested internal ilmo site"
    
    return render_template("sisainen.html")


@second_route("/sisainen/", methods=["POST"])
def sisainen_post():
    e_username = request.form.get("username")
    
    matrix.invite_user_to_rooms(f"@{e_username}:elokapina.fi")
    return "thank you"
