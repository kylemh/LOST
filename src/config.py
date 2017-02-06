import json
import os
import pathlib


# Create Secret Key
key = os.urandom(32)

# Global Variables
cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('config.base.json')

with cpath.open() as conf:
	c = json.load(conf)
	DB_NAME = c['database']['dbname']
	HOST = c['database']['dbhost']
	PORT = c['database']['dbport']

APP_SECRET_KEY = str(key)
DB_LOCATION = ('host=' + str(HOST) + ' port=' + str(PORT) + ' dbname=' + str(DB_NAME))
USERNAME = 'user'
PASSWORD = '123'
