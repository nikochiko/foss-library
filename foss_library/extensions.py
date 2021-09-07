from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect


csrf_protect = CSRFProtect()
db = SQLAlchemy()
flask_static_digest = FlaskStaticDigest()
migrate = Migrate()
