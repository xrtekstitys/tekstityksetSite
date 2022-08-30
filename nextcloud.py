import nextcloud_client
from config import config
class nextcloud():
    nc = nextcloud_client.Client(config.cloud_location)
    nc.login(config.nextcloud_username, config.nextcloud_password)
    def upload_file(save_path, server_path):
        nextcloud.nc.put_file(save_path, server_path)
        return "OK"
    def share_link(save_path):
        link = nextcloud.nc.share_file_with_link(save_path)
        link = link.get_link()
        return link
    def create_user(username, password):
        nextcloud.nc.create_user(username, password)
        return "OK"