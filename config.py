import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
is_prod = os.environ.get('IS_HEROKU', None)

# Production
if is_prod:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Local Development
else:
    SECRET_KEY = 'this_little_pig_went_to_the_market'
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/lost'
    DB_NAME = 'lost'
    HOST = 'localhost'
    PORT = '8080'
