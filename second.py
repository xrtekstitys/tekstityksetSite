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
from config import config # TODO #24 FIX THE IMPORTS

SECOND_DOMAIN = config.SECOND_DOMAIN
second = Blueprint("second", __name__)
second_route = partial(second.route, host=SECOND_DOMAIN)


@second_route("/")
def ilmoittaudu():
    handle.extra_debug(datas)
    datas = f"{request.remote_addr} reguested ilmosite"
    handle.extra_debug(datas)
    return render_template("ilmo.html")


@second_route("/ilmoittaudu/", methods=["POST"])
def ilmo_regi():
    etunimi = request.form.get("firstname")
    sukunimi = request.form.get("lastname")
    puhelin = request.form.get("phonenumber")
    telegram = request.form.get("telegram")
    whatsapp = request.form.get("whatsapp")
    litterointi = request.form.get("litterointi")
    kaantaminen = request.form.get("kaantaminen")
    datas = f"{request.remote_addr} posted following datas to ilmosite\n Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen}"
    handle.extra_debug(datas)
    f = open("ilmot.txt", "a")
    f.write(
        f"Etunimi:\n{etunimi}\nSukunimi:\n{sukunimi}\nPuhelin:\n{puhelin}\nTelegram: {telegram}\nWhatsapp: {whatsapp}\nLitterointi: {litterointi}\nKääntäminen: {kaantaminen},\n"
    )
    f.close()
    return "Otamme yhteyttä kun olemme katsoneet ilmoittautumisesi."


@second_route("/admin/")
def admin_panel():
    datas = f"{request.remote_addr} requested ilmo admin site"
    handle.extra_debug(datas)
    f = open("/root/nettisivu/ilmot.txt", "r")
    cat = f.read()
    f.close()
    cats = cat.split(",")
    return render_template("cat.html", cats=cats)


@second_route("/sisainen/")
def sisainen():
    datas = f"{request.remote_addr} requested internal ilmo site"
    handle.extra_debug(datas)
    return render_template("sisainen.html")


@second_route("/sisainen/", methods=["POST"])
def sisainen_post():
    e_username = request.form.get("username")
    handle.debug(request)
    matrix.invite_user_to_rooms(f"@{e_username}:elokapina.fi")
    return "thank you"
