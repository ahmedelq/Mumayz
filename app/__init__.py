from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

# ------- Standard Lib -------
import os


bootstrap = Bootstrap()


def app_factory(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)


    # ------ Blueprints ---------
    from app.main import main_bp 
    app.register_blueprint(main_bp)



    return app