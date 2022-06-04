from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
def send_debug(data):
    matrix_token = ""
    matrix_username = ""
    client = MatrixClient("", token=matrix_token, user_id=matrix_username)
    room_id = ""
    room = client.join_room(room_id)
    room.send_text(data)
