from matrix_client.client import MatrixClient
import nextcloud_client
# Matrix client things
matrix_token = ""
matrix_username = ""
room_id = ""
client = MatrixClient("https://matrix.elokapina.fi", token=matrix_token, user_id=matrix_username)
# Nextcloud client things
nextcloud_username = ""
nextcloud_password = ""
nc = nextcloud_client.Client('https://cloud.elokapina.fi/')
nc.login(nextcloud_username, nextcloud_password)