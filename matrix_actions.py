from config import (
    MATRIX_SERVER,
    MATRIX_TOKEN,
    ROOMS,
)
from matrix_api import (
    get_user_room, 
    invite_user, 
    send_message)
import requests
import json

class matrix:
    def create_room(element):
        room_id = get_user_room
        return room_id

    def send_message(room_id, message):
        send_message(room_id, message)
        return "OK"

    def invite_user_to_rooms(element):
        rooms = config.rooms
        for room in rooms:
            invite_user(element, room)
