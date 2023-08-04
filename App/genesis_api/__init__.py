from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from genesis_api.config import Config
import logging

# We create sqlalchemy instance
db = SQLAlchemy()

# Configure logging
logging.basicConfig(level=logging.INFO,)
formatter = logging.Formatter(
    '%(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# create app main function


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config.from_object(Config)

    # We initiate ORM
    db.init_app(app)

    app.app_context().push()

    from genesis_api.users.routes import user
    from genesis_api.image_classifier.routes import image_classifier

    app.register_blueprint(user)
    app.register_blueprint(image_classifier)

    return app
