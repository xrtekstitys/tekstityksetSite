from parse_config import *


# WEBSITE
UPLOAD_PATH = upload_path
DB = db
SSL = (pubkey, privkey)

# MATRIX
MATRIX_TOKEN = access_token
MATRIX_SERVER = matrix_url

CREATE_ACCOUNT_AUTH_TOKEN = account_creating_token
CREATE_ACCOUNT_SERVER_URL = account_creating_server
CREATE_ACCOUNT_SERVER_ENDING = account_creating_ending
CREATE_SECRET = account_creating_secret

# ROOMS
ROOM_ID = notification_room
ROOMS = wg
DEBUG_ROOM = debugger_room_id

# 2FA
VERIFICATION_ROOM_NAME = fa_room_name
ADMIN_2FA = admin_2fa

# NEXTCLOUD
NEXTCLOUD_USERNAME = nextcloud_username
NEXTCLOUD_PASSWORD = nextcloud_password
NEXTCLOUD_URL = nextcloud_url
CLOUD_LOCATION = NEXTCLOUD_URL

# MAINTANENCE & TESTMODE
MAINTANENCE_TRUE = maintanence_true
MAINTANENCE_IPS = maintanence_ips

# DOMAINS
MAIN_DOMAIN = main_domain
MAIN1_DOMAIN = second_domain
SECOND_DOMAIN = register_domain
JOIN_DOMAIN = joining_domain