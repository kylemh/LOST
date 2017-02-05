"""
NOTE:
1) the APP_SECRET_KEY is secret. it should be generated in a way that makes everyone comfortable.
   possible suggestions: A.) import os; os.urandom(size_bytes) B.) import uuid; str(uuid.uuid4())

2) DB_LOCATION is a string that can be passed to psycopg2 to connect to the db
"""

import os
import uuid

HOST = ""  # TODO: string
PORT= ""  # TODO: int
APP_SECRET_KEY = ""  #TODO: string, see note 1 above
DB_LOCATION = "" #TODO: string, see note 2 above
DEBUG = False