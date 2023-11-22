from flask import Flask


def create_app(test_config = None):
    app = Flask(__name__)
    app.secret_key = 'ffdddddd34lkdf0882sxxc'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app