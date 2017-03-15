import psycopg2
import csv
import sys


# Connect()
if len(sys.argv) > 1:
	DB_NAME = sys.argv[1]
else:
	DB_NAME = 'lost'
CONN = psycopg2.connect(dbname=DB_NAME, host='localhost', port=5432)
CUR = CONN.cursor()


def main():
	# Convert users, facilities, assets, and transfers tables to CSV files
	export_users()
	export_facilities()
	export_assets()
	export_transfers()

	# Close Postgres Database
	CUR.close()
	CONN.close()

	print('\nFinished database export!\n')
	return


def create_csv(csv_filename, header_list, sql_query_string):
	"""Transfer records from database query to a new .csv file.

    Keyword arguments:
    csv_filename -- String with a '.csv' suffix
    header_list -- List of strings (as CSV header names)
    sql_query_string -- Passed to match header_list format
    """

	with open(csv_filename, 'w', newline='\n') as csvfile:
		csv_writer = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(header_list)

		CUR.execute(sql_query_string)
		records = CUR.fetchall()
		CONN.commit()
		for entry in records:
			csv_writer.writerow(entry)


def export_users():
	fn = 'users.csv'
	header_names = ['username', 'password', 'role', 'active']
	query_string = "SELECT u.username, u.password, r.title, TRUE FROM users as u " \
				   "JOIN roles as r ON u.role_fk = r.role_pk;"

	create_csv(fn, header_names, query_string)
	print("\nUsers exported to", fn)
	return


def export_facilities():
	fn = 'facilities.csv'
	header_names = ['fcode', 'common_name']
	query_string = "SELECT fcode, common_name FROM facilities;"

	create_csv(fn, header_names, query_string)
	print("\nFacilities exported to", fn)
	return


def export_assets():
	fn = 'assets.csv'
	header_names = ['asset_tag', 'description', 'facility', 'acquired', 'disposed']
	query_string = "SELECT a.asset_tag, a.description, f.common_name, MIN(a_a.arrive_dt)::date, a_a.depart_dt::date " \
				   "FROM assets as a " \
				   "JOIN asset_at as a_a ON a.asset_pk = a_a.asset_fk " \
				   "JOIN facilities as f ON a_a.facility_fk = f.facility_pk " \
				   "GROUP BY a.asset_tag, a.description, f.common_name, a.disposed;"

	create_csv(fn, header_names, query_string)
	print("\nAssets exported to", fn)
	return


def export_transfers():
	fn = 'transfers.csv'
	header_names = ['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt']
	query_string = "SELECT a.asset_tag, requester.username, r.request_dt::date, " \
				   "approval_u.username, r.approve_dt::date, f1.fcode, f2.fcode, " \
				   "i_t.load_dt::date, i_t.unload_dt::date " \
				   "FROM assets as a " \
				   "JOIN requests as r ON a.asset_pk = r.asset_fk " \
				   "JOIN users as requester ON r.user_fk = requester.user_pk " \
				   "JOIN users as approval_u ON r.approving_user_fk = approval_u.user_pk " \
				   "JOIN facilities as f1 ON r.src_fk = f1.facility_pk " \
				   "JOIN facilities as f2 ON r.dest_fk = f2.facility_pk " \
				   "JOIN in_transit as i_t ON r.request_pk = i_t.request_fk;"

	create_csv(fn, header_names, query_string)
	print("\nTransfers exported to", fn)
	return


if __name__ == '__main__':
	main()
