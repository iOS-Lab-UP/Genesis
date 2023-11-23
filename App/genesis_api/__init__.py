from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from genesis_api.config import Config
from flask_cors import CORS
import logging
import redis

# Initialize SQLAlchemy and Redis clients
db = SQLAlchemy()

limiter = Limiter(
    storage_uri="redis://redis_rate_limiting:6379",
    key_func=get_remote_address
)

# Initialize cache config
cache = Cache(config={
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
})


# Initialize SocketIO
# Add CORS configuration as neede
socketio = SocketIO(cors_allowed_origins="*")


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
    Session(app)
    CORS(app)

    # Initialize Redis for rate-limiting

    app.app_context().push()

    # Initialize cache

    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from genesis_api.users.routes import user
    from genesis_api.image_classifier.routes import image_classifier
    from genesis_api.tools.routes import tools
    from genesis_api.medical_history.routes import medical_history
    from genesis_api.medicines.routes import medicines_endpoint

    app.register_blueprint(user)
    app.register_blueprint(image_classifier)
    app.register_blueprint(tools)
    app.register_blueprint(medical_history)
    app.register_blueprint(medicines_endpoint)

    return app
