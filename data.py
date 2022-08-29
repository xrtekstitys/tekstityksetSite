import os
import hashlib
from handler import handle
from config import config
from matrix_actions import matrix
import pickle
from werkzeug.utils import secure_filename
class data():
    def pickles(request):
        element = request.form.get("element")
        element_hash = hashlib.md5(bytes(element, 'utf-8')).hexdigest()
        if os.path.exists(config.db):
                with open(config.db, 'br') as file:
                    matrix_map = pickle.load(file)
                    if element_hash in matrix_map:
                        room_id = matrix_map[element_hash]
                        data = f"{request.remote_addr} with element {element} do have room for verification messages so creating one"
                        handle.extra_debug(data)
                        return room_id
                    else:
                        data = f"{request.remote_addr} with element {element} do not have room for verification messages yet so creating one"
                        handle.extra_debug(data)
                        room_id = matrix.create_room(element)
                        matrix_map[element_hash] = room_id
                        with open(config.db, 'bw') as file:
                            pickle.dump(matrix_map, file)
                        return room_id
        else:
            room_id = matrix.create_room(element)
            matrix_map = dict()
            matrix_map[element_hash] = room_id
            with open(config.db, 'bw') as file:
                pickle.dump(matrix_map, file)
            return room_id
    def save_video_info(filename, request):
        element = request.cookies.get('matrix')
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
        f.write(f"Element:\n{element} \nKäännökset:\nEnglanti:\n{englanti}\nRuotsi:\n{ruotsi}")
        f.close()
        return "OK"
    def save_video(file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(config.upload_path, filename))
        return "OK"
class texts():
    def new_video(link_info):
        new_video = f"Hei, uusi video on litteroitavana, videon linkki on: {link_info}.\nRakkautta ja raivoa, tekstitykset-bot."
        return new_video