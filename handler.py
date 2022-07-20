from matrix_actions import matrix
from config import config
from flask import render_template
class handle():
    def debug(request):
        data = f'ip {request.remote_addr} goed to site {request.path}'
        matrix.send_message(config.debug_room, data)
    def extra_debug(data):
        matrix.send_message(config.debug_room, data)
    def render_template(request, site):
        handle.debug(request)
        return render_template(site)