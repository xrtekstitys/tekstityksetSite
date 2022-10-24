from flask import Flask
import os
from config import (
    MAIN_DOMAIN,
    MAIN1_DOMAIN, 
    MAINTANENCE_TRUE,
    SSL
)
def create_app():
    APP_DOMAIN = MAIN_DOMAIN
    APP1_DOMAIN = MAIN1_DOMAIN
    response = requests.get("https://uptimerobot.com/inc/files/ips/IPv4.txt")
    UPTIMEROBOT_IPS = response.content
    app.logger.debug('Getting uptimerobot ips')
    app = Flask(__name__, host_matching=True, static_host=APP_DOMAIN)
    @app.before_request # Suoritetaan aina ennen pyyntöön vastaamista
    def before():
        if MAINTANENCE_TRUE == True:
            if request.remote_addr in UPTIMEROBOT_IPS or request.remote_addr in MAINTANENCE_IPS:
                app.logger.info("Letted user in, because user is from us or uptimerobot")
            else:
                abort(503)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route("/ping/")
    def ping():
        return 'pong'
    from . import id
    from . import second
    from . import index
    app.register_blueprint(second.second)
    app.register_blueprint(index.app1)
    app.register_blueprint(index.app2)
    app.register_blueprint(id.id)
    return app
def run_app():
    app = create_app()
    if __name__ == '__main__':
        return app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=SSL)