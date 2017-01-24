import psycopg2
import csv
import sys
import glob
from random import randint

def main():
    connect()
    conn.commit()

def connect():
    global conn

    try:
        conn = psycopg2.connect("host='localhost' port='" + port + "' dbname='" + db_name + "' user='osnapdev' password='secret'")
    except:
        print("Unable to connect to LOST Database")

def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')

if __name__ == '__main__':
    global db_name
    global port

    try:
        db_name = sys.argv[1]
        port = sys.argv[2]
    except UserWarning:
        print("Error with command line arguments. Connecting to lost:5432 anyways...")
    else:
        db_name = 'lost'
        port = '5432'

    main()
