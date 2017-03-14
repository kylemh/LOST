import psycopg2
import csv
import os
import glob
import sys

from config import DB_NAME, HOST, PORT

global CONN
global CUR


def main():
	"""Migration Driver. Return nothing."""
	connect()

	# Convert users, facilities, assets, and transfers tables to CSV files
	export_users()
	export_facilities()
	export_assets()
	export_transfers()

	# Close Postgres Database
	CONN.commit()
	CUR.close()
	CONN.close()

	print('\nFinished database export!\n')
	return


def create_csv(csv_filename, header_list):
	"""Take a filename with a csv suffix and a list of strings (as CSV header names). Return a CSV writer."""
	with open(csv_filename, 'w', newline='\n') as csvfile:
		csv_writer = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(header_list)

		records = CUR.execute("SELECT * FROM %s;", csv_filename[:-4]) # Filename without csv suffix
		return [records, csv_writer]


def connect():
	"""Open Postgres connection while migration runs."""
	CONN = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
	CUR = CONN.cursor()
	return


def export_users():
	fn = 'users.csv'
	header_names = ['username', 'password', 'role', 'active']
	data = create_csv(fn, header_names)

	for records, csv_writer in data:
		for row in records:
			username = row[2]
			password = row[3]
			CUR.execute("SELECT * FROM roles WHERE role_pk = %s;", row[1])
			role = CUR.fetchone()[1]
			active = 'TRUE'

			csv_writer.writerow([username, password, role, active])


def export_facilities():
	fn = 'facilities.csv'
	header_names = ['fcode', 'common_name']
	data = create_csv(fn, header_names)

	for records, csv_writer in data:
		for row in records:
			fcode = row[1]
			common_name = row[2]
			csv_writer.writerow([fcode, common_name])


def export_transfers():
	fn = 'transfers.csv'
	header_names = ['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt']
	data = create_csv(fn, header_names)

	for records, csv_writer in data:
		for row in records:

			# TODO: Fix query - Also, apply this design pattern to export_assets()
			query_string = "SELECT a.asset_tag, requester.username, r.request_dt, approval_u.username, r.approve_dt, f1.fcode, f2.fcode, i_t.load_dt, i_t.unload_dt " \
						   "FROM assets as a " \
						   "JOIN requests as r ON a.asset_pk = r.asset_fk " \
						   "JOIN users as requester ON r.user_fk = requester.user_pk " \
						   "JOIN users as approval_u ON r.approving_user_fk = approval_u.user_pk " \
						   "JOIN facilities as f1 ON r.src_fk = f1.facility_pk " \
						   "JOIN facilities as f2 ON r.dest_fk = f2.facility_pk " \
						   "JOIN in_transit as i_t ON r.request_pk = i_t.request_fk;"
			CUR.execute()

			CUR.execute("SELECT * FROM assets WHERE asset_pk = %s;", row[1])
			asset_tag = CUR.fetchone()[1]
			print('\n\nThis is asset_tag:', asset_tag) # DEBUG

			CUR.execute("SELECT * FROM users WHERE user_pk = %s;", row[2])
			request_by = CUR.fetchone()[2]
			print('\n\nThis is request_by:', request_by) # DEBUG

			request_dt = row[5]
			print('\n\nThis is request_dt', request_dt) # DEBUG

			approved = CUR.execute("SELECT * FROM requests WHERE user_fk = %s AND approved = TRUE;", row[2])
			if not approved:
				approve_by = 'NULL'
				approve_dt = 'NULL'
			else:
				fetch = CUR.fetchone()
				approve_by = fetch[2]
				approve_dt = fetch[6]

			CUR.execute("SELECT * FROM facilities WHERE facility_pk = %s;", row[3])
			source = CUR.fetchone()[1]
			CUR.execute("SELECT * FROM facilities WHERE facility_pk = %s;", row[4])
			destination = CUR.fetchone()[1]

			# TODO
			CUR.execute("SELECT load_dt, unload_dt FROM in_transit")
			load_dt = None
			unload_dt = None

			csv_writer.writerow([asset_tag, request_by, request_dt, approve_by, approve_dt, source, destination, load_dt, unload_dt])
