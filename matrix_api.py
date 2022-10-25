import requests
import json
import time
from config import (
    MATRIX_URL, 
    VERSION, 
    USERNAME)

def request(method: str, path: str, payload="{}"):
    url = f"/_matrix/client/{VERSION}/{path}"
    headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
    }
    response = requests.request(method, url, headers=headers, data=payload)
    if not response.status_code == 429:
        return response
    else:
        time.sleep(3)
        return request(method, path, payload=payload)

def create_dm(user: str):
    payload = json.dumps({
    "is_direct": True,
    "invite": [
        user
    ],
    "preset": "trusted_private_chat"
    })

    response = request("POST", "createRoom", payload=payload)
    return response.json()["room_id"]

def get_user_room(user):
    response = request("GET", f"user/{USERNAME}/account_data/m.direct")
    if user in response.json():
        return response.json()[user][0]
    else:
        return create_dm(user)

def invite_user(user, roomid):
    payload = json.dumps({
    "reason": "You joined to working group using website",
    "user_id": user
    })
    response = request("POST", F"rooms/{roomid}/invite", payload=payload)

def send_message(roomid, message):
    payload = json.dumps({
    "msgtype": "m.text",
    "body": message,
    "mimetype": "text/html"
    })
    
    headers = {
    'Content-Type': 'application/json'
    }

    request("POST", f"rooms/{roomid}/send/m.room.message", payload=payload)

