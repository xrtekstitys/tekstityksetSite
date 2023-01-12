import json
import pyotp

def get_otp():
    with open("otp.json", "r") as f:
        data = json.load(f)
    return data


def is_otp_right(username, otp):
    data = get_otp()
    if data[username] == otp:
        return True
    return False


def create_otp(username):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    totp = totp.now()
    data = get_otp()
    data[username] = totp
    
    with open("otp.json", "w") as f:
        json.dump(data, f)

    return totp
