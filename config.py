from yaml1 import *


# WEBSITE
UPLOAD_PATH = website.upload_path
DB = website.db
SSL = (website.pubkey, website.privkey)

# MATRIX
MATRIX_TOKEN = matrix.access_token
MATRIX_SERVER = matrix.url

CREATE_ACCOUNT_AUTH_TOKEN = website.account_creating_token
CREATE_ACCOUNT_SERVER_URL = website.account_creating_server
CREATE_ACCOUNT_SERVER_ENDING = website.account_creating_ending
CREATE_SECRET = website.account_creating_secret

# ROOMS
ROOM_ID = website.notification_room
ROOMS = website.wg
DEBUG_ROOM = debugger.room_id

# 2FA
VERIFICATION_ROOM_NAME = website.admin_2fa
ADMIN_2FA = website.admin_2fa

# NEXTCLOUD
NEXTCLOUD_USERNAME = nextcloud.username
NEXTCLOUD_PASSWORD = nextcloud.password
NEXTCLOUD_URL = nextcloud.url
CLOUD_LOCATION = NEXTCLOUD_URL
# MAINTANENCE & TESTMODE
TESTMODE = debugger.testmode
MAINTANENCE = debugger.maintanence
TESTMODE_TRUE = testmode.testmode_true
MAINTANENCE_TRUE = debugger.maintanence_true
TESTMODE_IPS = testmode.testmode_ips
MAINTANENCE_IPS = debugger.maintanence_ips

# DOMAINS
MAIN_DOMAIN = website.main_domain
TEST_MAIN_DOMAIN = testmode.test_main_domain
MAIN1_DOMAIN = website.second_domain
TEST_MAIN1_DOMAIN = testmode.test_second_domain
SECOND_DOMAIN = website.register_domain
TEST_SECOND_DOMAIN = testmode.test_register_domain
TEST_JOIN_DOMAIN = testmode.test_join_domain
JOIN_DOMAIN = website.joining_domain