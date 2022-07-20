#!/usr/bin/env python

import yaml
class config():
    with open('/root/nettisivu/user.yaml') as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in docs:
            debugger = doc["Debugger"]
            matrix = doc["Matrix"]
            nextcloud = doc["Nextcloud"]
            website = doc["Website"]
class debugger():
    debuggeri = config.debugger
    matrix = debuggeri['Matrix']
    enabled = matrix['Enabled']
    room_id = matrix['Room_id']
class matrix():
    matrixi = config.matrix
    server = matrixi["Server"]
    url = server["Url"]
    user = matrixi["User"]
    access_token = user["Access_token"]
class nextcloud():
    cloudi = config.nextcloud
    server = cloudi["Server"]
    url = server["Url"]
    user = cloudi["User"]
    username = user["Username"]
    password = user["Password"]
class website():
    websaitti = config.website
    domains = websaitti["Domains"]
    main_domain = domains["Main_domain"]
    second_domain = domains["Second_domain"]
    register_domain = domains["Register_domain"]
    joining_domain = domains["Joining_domain"]
    rooms = websaitti["Rooms"]
    notification_room = rooms["Notification"]
    fa_room = rooms["2fa_room"]
    fa_room_name = fa_room["name"]
    wg = rooms["WG"]
    paths = websaitti["Paths"]
    upload_path = paths["Upload"]
    db = paths["DB"]
    secrets = websaitti["Secrets"]
    admin = secrets["Admin"]
    admin_2fa = admin["2FA"]
    account = secrets["Account"]
    account_creating = account["Creating"]
    account_creating_enabled = account_creating["Enabled"]
    account_creating_token = account_creating["Token"]
    account_creating_server = account_creating["Server"]
    account_creating_ending = account_creating["Ending"]
    account_creating_secret = account_creating["Secret"]
    SSL = secrets["SSL"]
    privkey = SSL['privkey']
    pubkey = SSL['pubkey']




