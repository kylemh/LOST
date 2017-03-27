from flask import redirect, url_for
from datetime import datetime
import psycopg2

DB_NAME = 'lost'
HOST = 'localhost'
PORT = '8080'


# MARK: DATABASE FUNCTIONS
def db_query(sql, data_list):
    """Returns none or a list of tuples from a SQL query and passed values."""
    conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute(sql, data_list)

    # Return data as an array of dictionaries
    result = cur.fetchall()
    records = []

    # If the query returns something...
    if len(result) != 0:
        entries = result
        for row in entries:
            records.append(row)
    else:
        # No results in query
        return None

    conn.commit()
    cur.close()
    conn.close()
    return records


def db_change(sql, data_list):
    """Updates database using passed INSERT or UPDATE SQL command and vars."""
    conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
    cur = conn.cursor()
    try:
        cur.execute(sql, data_list)
    except Exception as e:
        print("QUERY FAILED")
        print(e)
        redirect(url_for('failed_query'))

    conn.commit()
    cur.close()
    conn.close()


def duplicate_check(sql, data_list):
    """Returns True if a query yields a result and False if not."""
    conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute(sql, data_list)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        return True
    else:
        return False


def validate_date(date):
    """Confirms that user entered a date in the MM/DD/YYYY format."""
    try:
        date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        return date
    except ValueError:
        raise ValueError('Incorrect data format, should be MM/DD/YYYY')
