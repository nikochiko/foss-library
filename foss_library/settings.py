"""
Application configuration.

Can be set via environment variables, or a .env file
"""
from environs import Env

env = Env()

ENV = env.str("FLASK_ENV", default="production")

if ENV.lower() == "testing":
    env.read_env("foss_library/testing.env")
else:
    env.read_env()

DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=300)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False

if ENV.lower() == "testing":
    WTF_CSRF_ENABLED = False
    assert SQLALCHEMY_DATABASE_URI.endswith(
        "_test"
    ), "DATABASE_URL should end in _test in testing environment"
