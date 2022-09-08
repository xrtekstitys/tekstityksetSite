from flask import Flask
import os
from config import config
def create_app():
    if config.testmode_true == True:
        MAIN_DOMAIN = config.TEST_MAIN_DOMAIN
        MAIN1_DOMAIN = config.TEST_MAIN1_DOMAIN
    else:
        MAIN_DOMAIN = config.MAIN_DOMAIN
        MAIN1_DOMAIN = config.MAIN1_DOMAIN
    app = Flask(__name__, host_matching=True, static_host=MAIN_DOMAIN)
    @app.before_first_request
    def before_first():
        response = requests.get("https://uptimerobot.com/inc/files/ips/IPv4.txt")
        uptimerobot_ips = response.content
        app.logger.debug('Getting uptimerobot ips')
    @app.before_request # Suoritetaan aina ennen pyyntöön vastaamista
    def before():
        handle.debug(request)
        if config.testmode_true == True or config.maintanence_true == True:
            if request.remote_addr in uptimerobot_ips or request.remote_addr in config.testmode_ips or request.remote_addr in config.maintanence_ips:
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
        if config.testmode_true == True:
            app.run(host=TEST_MAIN_DOMAIN, port=443, debug=True, threaded=True,ssl_context=config.ssl)
        else:
            app.run(host=MAIN_DOMAIN, port=443, debug=False, threaded=True,ssl_context=config.ssl)