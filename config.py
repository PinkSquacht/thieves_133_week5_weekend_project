import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')