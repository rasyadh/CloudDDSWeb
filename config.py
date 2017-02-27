import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    domain_url = "http://localhost:5000/"
    DEBUG       = False
    TESTING     = False
    CSRF_ENABLED= True
    SECRET_KEY  = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cloudservice.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'cloudtelkomdds'
    MAIL_PASSWORD = 'Admintelk0m'
    MAIL_DEFAULT_SENDER = 'cloudtelkomdds@gmail.com'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
