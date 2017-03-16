import json
import os
import pathlib


APP_SECRET_KEY = str(os.urandom(32))

# Global Variables
basedir = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')
with basedir.open() as conf:
    c = json.load(conf)
    DB_NAME = c['database']['dbname']
    HOST = c['database']['dbhost']
    PORT = c['database']['dbport']
