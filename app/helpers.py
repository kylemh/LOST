from flask import redirect, url_for
import datetime
import psycopg2
import bcrypt

from config import SQLALCHEMY_DATABASE_URI


# DATABASE FUNCTIONS
def db_query(sql, data_list):
    """Returns none or a list of tuples from a SQL query and passed values."""
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()
    cur.execute(sql, data_list)

    # Return data as an array of dictionaries
    result = cur.fetchall()
    records = []

    # If the query returns something...
    if len(result) != 0:
        for row in result:
            records.append(row)
        conn.commit()
        cur.close()
        conn.close()
        return records
    else:
        conn.commit()
        cur.close()
        conn.close()
        return None


def db_change(sql, data_list):
    """Updates database using passed INSERT or UPDATE SQL command and vars."""
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
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
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()
    cur.execute(sql, data_list)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        return True
    else:
        return False


def validate_date(submitted_date):
    """Confirms that user entered a date in the MM/DD/YYYY format."""
    try:
        submitted_date = datetime.datetime.strptime(submitted_date, '%m/%d/%Y').date()
        return submitted_date
    except ValueError:
        raise ValueError('Incorrect data format, should be MM/DD/YYYY')


# AUTHORIZATION FUNCTIONS
def _get_hash_for_user(username):
    password = bytes(db_query("SELECT password FROM users WHERE username=%s;", [username])[0][0])
    return password


def _get_salt_for_user(username):
    salt = bytes(db_query("SELECT salt FROM users WHERE username=%s;", [username])[0][0])
    return salt


def _create_password_hash(password):
    salt = bcrypt.gensalt(16)
    hashed_pass = bcrypt.hashpw(password, salt)
    return hashed_pass, salt


def _check_hash_for_user(username, password):
    stored_hash = _get_hash_for_user(username)
    generated_hash = _recreate_hash(password, _get_salt_for_user(username))
    return stored_hash == generated_hash


def _recreate_hash(password, salt):
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass


def authorize(username, password):
    return _check_hash_for_user(username, password)
