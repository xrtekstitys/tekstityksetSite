import yaml
class config():
    with open('./config.yaml') as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in docs:
            debugger = doc["Debugger"]
            matrix = doc["Matrix"]
            nextcloud = doc["Nextcloud"]
            website = doc["Website"]

# MAIN CONFIG
debugger = config.debugger
matrix = config.matrix
website = config.website
cloud = config.nextcloud

# DEBUGGER
matrix = debugger['Matrix']
maintanence = debugger["Maintanence"]

# MATRIX
matrix_url = matrix["Server"]["Url"]

# USER
access_token = matrix["User"]["Access_token"]

matrix_enabled = matrix['Enabled']
debugger_room_id = matrix['Room_id']

# MAINTANENCE
maintanence_true = maintanence["Enabled"]
maintanence_ips = maintanence["Allowed_ip_list"]

# NEXTCLOUD
nextcloud_url = cloud["Server"]["Url"]
nextcloud_username = ["User"]["Username"]
nextcloud_password = ["User"]["Password"]

# website
rooms = website["Rooms"]
secrets = website["Secrets"]
domains = website["Domains"]
paths = website["Paths"]

# Secrets
admin = secrets["Admin"]
account = secrets["Account"]
SSL = secrets["SSL"]

# Domains
main_domain = domains["Main_domain"]
second_domain = domains["Second_domain"]
register_domain = domains["Register_domain"]
joining_domain = domains["Joining_domain"]

# Rooms
notification_room = rooms["Notification"]
fa_room_name = rooms["2fa_room"]["name"]
wg = rooms["WG"]

# Account creating
account_creating_enabled = account["Creating"]["Enabled"]
account_creating_token = account["Creating"]["Token"]
account_creating_server = account["Creating"]["Server"]
account_creating_ending = account["Creating"]["Ending"]
account_creating_secret = account["Creating"]["Secret"]

# Paths
upload_path = paths["Upload"]
db = paths["DB"]

# Admin things
admin_2fa = admin["2FA"]




# SSL
privkey = SSL['privkey']
pubkey = SSL['pubkey']