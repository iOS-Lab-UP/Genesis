from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from genesis_api.config import Config
import logging
import redis

# Initialize SQLAlchemy and Redis clients
db = SQLAlchemy()

limiter =Limiter(
    storage_uri="redis://redis_rate_limiting:6379",
    key_func=get_remote_address
)



# Configure logging
logging.basicConfig(level=logging.INFO,)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize ORM
    db.init_app(app)
    limiter.init_app(app)

    # Initialize Redis for user sessions
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'your_prefix:'
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis', port=6380, decode_responses=True)
    Session(app)

    # Initialize Redis for rate-limiting

    app.app_context().push()

    from genesis_api.users.routes import user
    from genesis_api.image_classifier.routes import image_classifier
    from genesis_api.tools.routes import tools

    app.register_blueprint(user)
    app.register_blueprint(image_classifier)
    app.register_blueprint(tools)

    return app
