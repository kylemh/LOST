import json
import os
import pathlib


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    APP_SECRET_KEY = str(os.urandom(32))
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # Global Variables
    basedir = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')
    with basedir.open() as conf:
        c = json.load(conf)
        DB_NAME = c['database']['dbname']
        HOST = c['database']['dbhost']
        PORT = c['database']['dbport']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


# class DevelopmentConfig(Config):
# 	DEVELOPMENT = True
# 	DEBUG = True
#
#
# class TestingConfig(Config):
# 	TESTING = True
