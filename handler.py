from matrix_actions import matrix
from config import (DEBUG_ROOM)
from flask import render_template
class handle():
    def debug(request):
        data = f'ip {request.remote_addr} goed to site {request.path}'
        matrix.send_message(DEBUG_ROOM, data)
    def extra_debug(data):
        matrix.send_message(DEBUG_ROOM, data)
    def render_template(request, site):
        handle.debug(request)
        return render_template(site)