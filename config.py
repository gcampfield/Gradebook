import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\xce!\xca4k\xcf\x89\xeb\xf7xxM\xf2\xb6/\xa6/\xb7\xf9\x82\x92\xc8\x8c'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
