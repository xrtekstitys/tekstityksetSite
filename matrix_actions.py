from api import MatrixHttpApi
from config import (
    MATRIX_SERVER,
    MATRIX_TOKEN,
    ROOMS,
    CREATE_ACCOUNT_SERVER_URL,
    CREATE_ACCOUNT_SERVER_ENDING,
    CREATE_ACCOUNT_AUTH_TOKEN,
)
import requests
import json


class matrix:
    matrix_account = MatrixHttpApi(MATRIX_SERVER, token=MATRIX_TOKEN)

    def create_room(element):
        room = MatrixHttpApi.create_room(matrix.matrix_account, False, [element])
        room_id = str(room).replace("{'room_id': '", "")
        room_id = str(room_id).replace("'}", "")
        print(room)
        return room_id

    def change_name(room_id, name):
        MatrixHttpApi.set_room_name(matrix.matrix_account, room_id, name)
        return "OK"

    def invite_user(room_id, element):
        MatrixHttpApi.invite_user(matrix.matrix_account, room_id, element)
        return "OK"

    def send_message(room_id, message):
        MatrixHttpApi.send_message(matrix.matrix_account, room_id, message)
        return "OK"

    def invite_user_to_rooms(element):
        rooms = config.rooms
        for room in rooms:
            matrix.invite_user(room, element)

    def create_user(request):
        username = request.form.get("username")
        password = request.form.get("password")
        url = f"{CREATE_ACCOUNT_SERVER_URL}/_synapse/admin/v2/users/@{username}:{CREATE_ACCOUNT_SERVER_ENDING}"
        payload = json.dumps(
            {
                "password": f"{password}",
                "admin": False,
                "deactivated": False,
                "user_type": None,
            }
        )
        headers = {
            "Authorization": f"Bearer {CREATE_ACCOUNT_AUTH_TOKEN}",
            "Content-Type": "application/json",
        }

        requests.request("PUT", url, headers=headers, data=payload)
        return "OK"
