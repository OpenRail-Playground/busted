import os

class Config:
    PROJECT = "busted"
    PROJECT_NAME = "https://github.com/OpenRail-Playground/busted"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_INSTANCE_PATH = os.path.join(PROJECT_ROOT, "instance")
    DATABASE = os.path.join(PROJECT_INSTANCE_PATH, 'busted-test.sqlite')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(PROJECT_INSTANCE_PATH, 'busted.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
