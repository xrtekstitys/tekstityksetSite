import nextcloud_client
from config import CLOUD_LOCATION, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD


class nextcloud:
    nc = nextcloud_client.Client(CLOUD_LOCATION)
    nc.login(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

    def upload_file(self, save_path, server_path):
        nextcloud.nc.put_file(save_path, server_path)
        return "OK"

    def share_link(self, save_path):
        link = nextcloud.nc.share_file_with_link(save_path)
        link = link.get_link()
        return link

    def create_user(self, username, password):
        nextcloud.nc.create_user(username, password)
        return "OK"
