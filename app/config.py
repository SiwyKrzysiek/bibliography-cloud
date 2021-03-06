import os
import secrets
from dotenv import load_dotenv
import redis

from users import UserManager
from login import LoginManager

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(128)
    DEBUG = bool(os.environ.get('DEBUG')) or False

    REDIS_NAME = os.environ.get('REDIS_NAME') or 'localhost'
    REDIS_URL = f'redis://{REDIS_NAME}'

    JWT_SECRET = os.environ.get(
        'JWT_SECRET') or 'ChangeMeChangeMeChangeMeChangeMeChangeMeChangeMeChangeMeChangeMeChangeMe'
    JWT_SESSION_TIME = int(os.environ.get('JWT_SESSION_TIME') or '4')

    APP_URL = os.environ.get('APP_URL') or 'http://localhost:5000'

    FILE_STORE_HOST = os.environ.get('FILE_STORE_HOST') or 'localhost'
    FILE_STORE_URL = f'http://{FILE_STORE_HOST}:8081'

    PUBLICATION_API_HOST = os.environ.get(
        'PUTLICATION_API_HOST') or 'localhost'
    PUBLICATION_API_URL = f'http://{PUBLICATION_API_HOST}:8090'

    redis = redis.Redis(REDIS_NAME)
    # user_manager = UserManager(redis)
    login_manager = LoginManager(redis)

    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_API_BASE_URL = os.environ.get('AUTH0_API_BASE_URL')
    AUTH0_CALLBACK_URL = APP_URL + '/callback'
