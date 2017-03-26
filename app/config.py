import json
import os
import pathlib


class Config(object):
    APP_SECRET_KEY = 'this_little_pig'
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/lost'

    # Global Variables
    basedir = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')
    with basedir.open() as conf:
        c = json.load(conf)
        DB_NAME = c['database']['dbname']
        HOST = c['database']['dbhost']
        PORT = c['database']['dbport']
