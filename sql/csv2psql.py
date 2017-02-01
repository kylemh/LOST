import psycopg2
import csv
import sys
import glob

# TODO: Implement more extensible format

def main():
	# Connect to database
	conn = "host='localhost' port='" + port + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
	print("Connecting to database\n ->%s" % conn)
	db = psycopg2.connect(conn)
	print("CONNECTION COMPLETE")

	# Create database cursor
	global cur
	cur = db.cursor()

	# Increase work memory
	work_mem = 1024
	cur.execute('SET work_mem TO ' + str(work_mem))

	# Translate legacy data into useful information for facilities and inventory for each facility
	facilities()

	# TODO: Populate Products, Levels, Compartments, and Security Tags

	# Commit changes to database
	db.commit()


def facilities():
	for fn in glob.iglob('./osnap_legacy/**/*.csv', recursive=True):
		if "inventory" in fn:
			fcode = fn.split('/')[2].split('_')[0]

			# Translate facility code into understandable data
			# TODO: Ensure common names and locations are correctly translated
			if fcode == "HQ":
				common_name = "Headquarters"
				location = "Eugene, OR"
			elif fcode == "DC":
				common_name = "The Capitol"
				location = "Washington, D.C."
			elif fcode == "SPNV":
				common_name = "Sparks Nevada"
				location = "Sparks, NV"
			elif fcode == "NC":
				common_name = "National City"
				location = "National City, CA"
			else:
				common_name = fcode
				location = "UNDISCLOSED"

			insert("facilities", ["fcode", "common_name", "location"], [fcode, common_name, location])
			cur.execute("SELECT facility_pk FROM facilities WHERE fcode = '" + fcode + "';")
			facility_pk = cur.fetchone()[0]
			inventory(fn, facility_pk)


def inventory(fn, facility_fk):
	reader = csv.reader(open(fn, newline=''), delimiter=',', quotechar='|')
	head = next(reader)
	for row in reader:
		insert("assets", ["asset_tag", "description"], [row[0], row[2]])
		cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = '" + row[0] + "';")
		asset_fk = cur.fetchone()[0]
		insert("asset_at", ["asset_fk", "facility_fk"], [asset_fk, facility_fk])


# TODO: Define get_pk(table, columns, values)
def get_pk(table, columns, values):
	# UNIMPLEMENTED
	return


def insert(table, columns, values):
	column_string = ','.join(columns)
	value_string = ""

	for i in range(len(values)):
		if type(values[i]) == str:
			value_string += ("'" + values[i] + "'")
		else:
			value_string += (str(values[i]))

		if i != (len(values) - 1):
			value_string += ","

	sql_insert = "INSERT INTO {}({}) VALUES ({});".format(table, column_string, value_string)
	cur.execute(sql_insert)


if __name__ == '__main__':
	global db_name
	global port

	try:
		db_name = sys.argv[1]
		port = int(sys.argv[2])
	except:
		print("\nError with command line arguments!\nConnecting to lost:5432 anyways...\n")
		db_name = 'lost'
		port = '5432'
	else:
		print("\nYou entered incorrect arguments...\n")
		db_name = 'lost'
		port = '5432'

	main()
