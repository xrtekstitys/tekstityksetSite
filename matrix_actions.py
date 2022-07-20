from api import MatrixHttpApi
from config import config
import requests
import json
class matrix():
    matrix_account = MatrixHttpApi(config.matrix_server, token=config.matrix_token)
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
        url = f"{config.create_account_server_url}/_synapse/admin/v2/users/@{username}:{config.create_account_server_ending}"
        payload = json.dumps({
        "password": f"{password}",
        "admin": False,
        "deactivated": False,
        "user_type": None
        })
        headers = {
        'Authorization': f'Bearer {config.create_account_auth_token}',
        'Content-Type': 'application/json'
        }

        requests.request("PUT", url, headers=headers, data=payload)
        return "OK"