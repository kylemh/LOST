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


def balance(a, b, c, d):
    sum = a + b + c + d
    if sum == 1:
        a = 1
        b = 0
        c = 0
        d = 0
    elif sum == 2:
        a = 1
        b = 1
        c = 0
        d = 0
    elif sum == 3:
        a = 1
        b = 1
        c = 1
        d = 0
    elif sum == 4:
        a = 1
        b = 1
        c = 1
        d = 1
    elif sum > 4:
        base = sum / 4
        remainder = sum % 4





# Input a=1, b=2, c=3, d=10
# Output a=4, b=4, c=4, d=4
# Ouput:
#     Move 3 from d to a
#     Move 2 from d to b
#     Move 1 from d to c
#
# Input a=1, b=2, c=0, d=0
# Ouput a=1, b=1, c=1, d=0
# Output:
#     Move 1 from b to c
#
# Input a=1, b=0, c=0, d=0
# Output a=1, b=0, c=0, d=0
# Output:
#     Move None