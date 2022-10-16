from parse_config import *

# WEBSITE
UPLOAD_PATH = "./static/uploads/"
DB = "./datas.pickle"
SSL = ("PUBKEY_PATH", "PRIV_PATH")

# MATRIX
MATRIX_TOKEN = "syttoken"
MATRIX_SERVER = "https://matrix.org"

# ROOMS
ROOM_ID = "!roomid:matrix.org"
ROOMS = ["!someroomid:matrix.org", "!somespaceid:matrix.org"]
DEBUG_ROOM = "!debugroomid:matrix.org"

# 2FA
VERIFICATION_ROOM_NAME = "VERIFICATION"
ADMIN_2FA = "ADMIN_2FA"

# NEXTCLOUD
NEXTCLOUD_USERNAME = "nextcloud"
NEXTCLOUD_PASSWORD = "password"
NEXTCLOUD_URL = "nextcloud.com"
CLOUD_LOCATION = NEXTCLOUD_URL

# MAINTANENCE & TESTMODE
MAINTANENCE_TRUE = False
MAINTANENCE_IPS = "1.1.1.1"

# DOMAINS
MAIN_DOMAIN = "example.org"
MAIN1_DOMAIN = "example.com"
SECOND_DOMAIN = "second.example.org"
JOIN_DOMAIN = "ilmo.example.org"