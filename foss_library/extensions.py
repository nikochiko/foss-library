from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


csrf_protect = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
