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
	file = DIR + 'users.csv'
	users_query = "INSERT INTO users (role_fk, username, password, active) VALUES (%s, %s, %s, TRUE);"

	with open(file) as csvfile:
		rows = csv.DictReader(csvfile)

		for record in rows:
			CUR.execute(users_query, (record['role'], record['username'], record['password'], record['active']))

		CONN.commit()


def import_facilities():
	file = DIR + 'facilities.csv'
	facilities_query = "INSERT INTO facilities (fcode, common_name) VALUES (%s, %s);"

	with open(file) as csvfile:
		rows = csv.DictReader(csvfile)

		for record in rows:
			CUR.execute(facilities_query, (record['fcode'], record['common_name']))

		CONN.commit()


def import_assets():
	file = DIR + 'assets.csv'
	assets_query = "INSERT INTO assets (asset_tag, description, disposed) VALUES (%s, %s, %s);"
	asset_at_query = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) VALUES " \
					 "((SELECT asset_pk FROM assets WHERE asset_tag = %s), " \
					 "(SELECT facility_pk FROM facilities WHERE fcode = %s), %s, %s)"

	with open(file) as csvfile:
		rows = csv.DictReader(csvfile)

		for record in rows:
			CUR.execute(assets_query, record['asset_tag'], record['description'], record['disposed'])
			CUR.execute(asset_at_query, [record['asset_tag'], record['facility_fk']])

		CONN.commit()


def import_transfers():
	file = DIR + 'transfers.csv'
	transfers_query = "INSERT INTO "



if __name__ == '__main__':
	main()
