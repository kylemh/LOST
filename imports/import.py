import csv
import sys
import psycopg2


# Connect()
if len(sys.argv) > 2:
	DB_NAME = sys.argv[1]
	DIR = sys.argv[2]
	if DIR != '' and DIR[-1] != '/':
		DIR += '/'
else:
	DB_NAME = 'lost'
	DIR = 'data/'
CONN = psycopg2.connect(dbname=DB_NAME, host='localhost', port=5432)
CUR = CONN.cursor()


def main():
	# Convert users, facilities, assets, and transfers tables to CSV files
	import_users()
	import_facilities()
	import_assets()
	import_transfers()

	# Close Postgres Database
	CUR.close()
	CONN.close()

	print('\nFinished database import!\n')
	return


def import_users():
	location = DIR + 'users'
	query = "INSERT INTO users (role_fk, username, password, active) VALUES (%s, %s, %s, TRUE);"




def import_facilities():
	location = DIR + 'facilities'
	query = "INSERT INTO facilities (fcode, common_name) VALUES (%s, %s);"


def import_assets():
	location = DIR + 'assets'
	query = "INSERT INTO assets (asset_tag, description, disposed) VALUES (%s, %s, %s);"


def import_transfers():
	location = DIR + 'transfers'
	query = "INSERT INTO "

if __name__ == '__main__':
	main()
