from yaml1 import *
class config():
    room_id = website.notification_room
    rooms = website.wg
    MAIN_DOMAIN = website.main_domain
    MAIN1_DOMAIN = website.second_domain
    SECOND_DOMAIN = website.register_domain
    JOIN_DOMAIN = website.joining_domain
    matrix_token = matrix.access_token
    matrix_server = matrix.url
    debug_room = debugger.room_id
    upload_path = website.upload_path
    db = website.db
    cloud_location = nextcloud.url
    nextcloud_username = nextcloud.username
    nextcloud_password = nextcloud.password
    admin_2fa = website.admin_2fa
    create_secret = website.account_creating_secret
    ssl = (website.pubkey, website.privkey)
    verification_room_name = website.admin_2fa
    create_account_auth_token = website.account_creating_token
    create_account_server_url = website.account_creating_server
    create_account_server_ending = website.account_creating_ending