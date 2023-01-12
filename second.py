from flask import (
    Blueprint,
    render_template,
    request,
)
from config import (SECOND_DOMAIN)
from functools import partial
from matrix_actions import matrix
second = Blueprint("second", __name__)
second_route = partial(second.route, host=SECOND_DOMAIN)


@second_route("/")
def sisainen():
    return render_template("sisainen.html")


@second_route("/sisainen/", methods=["POST"])
def sisainen_post():
    e_username = request.form.get("username")

    matrix.invite_user_to_rooms(f"@{e_username}:elokapina.fi")
    return "thank you"
