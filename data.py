import os
import hashlib

from config import UPLOAD_PATH
from matrix_actions import matrix
from werkzeug.utils import secure_filename

import json


def get_rooms():
    with open("rooms.json", "r") as f:
        data = json.load(f)
    return data


def get_room_id(username):
    data = get_rooms()
    username_hash = get_username_hash(username)

    if username_hash in data:
        room_id = data[username_hash]
    else:
        room_id = matrix.create_room(username)
        set_room_id(username, room_id)
    return room_id


def get_username_hash(username):
    username_hash = hashlib.md5(bytes(username, "utf-8")).hexdigest()
    return username_hash


def set_room_id(username, room_id):
    data = get_rooms()
    data[get_username_hash(username)] = room_id
    with open("rooms.json", "w") as f:
        json.dump(data, f)


class data:
    def save_video_info(filename, request):
        element = request.cookies.get("matrix")
        englanti = request.form.get("English")
        ruotsi = request.form.get("Sweden")
        if englanti == "English":
            englanti = "Halutaan"
        elif englanti == "None":
            englanti = "Ei haluta"
        if ruotsi == "Sweden":
            ruotsi = "Halutaan"
        elif ruotsi == "None":
            ruotsi = "Ei haluta"
        f = open(f"{filename}.txt", "w")
        f.write(
            f"Element:\n{element} \nKäännökset:\nEnglanti:\n{englanti}\nRuotsi:\n{ruotsi}"
        )
        f.close()
        return "OK"

    def save_video(file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_PATH, filename))
        return "OK"


class texts:
    def new_video(link_info):
        return f"Hei, uusi video on litteroitavana, videon linkki on: {link_info}.\nRakkautta ja raivoa, tekstitykset-bot."
