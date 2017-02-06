import psycopg2
import csv
import sys
import glob

def main():
	# Translate legacy data into useful information
	# Security Data
	with open('sec_load.sql', 'w') as f:
		process_levels(f)
		process_compartments(f)

	# Facilities and Inventory Data
	facilities() #inventory() gets called within

	# Product Data
	with open('prod_load.sql', 'w') as f:
		process_products(f)

	with open('prod_load.sql', 'w') as f:
		process_products(f)


	# Inventory Data
	# TODO: Populate Products, Levels, Compartments, and Security Tags

	# Commit changes to database
	db.commit()


############################
# SECURITY DATA PROCESSING #
############################
def process_levels(outf):
	with open('osnap_legacy/security_levels.csv') as f:
		data = csv.DictReader(f)
		i = 5
		for r in data:
			outf.write("INSERT INTO sec_levels (level_pk,abbrv,comment) VALUES (%s,'%s','%s');\n"%(i,r['level'],r['description']))
			i = i-1

def process_compartments(outf):
	with open('osnap_legacy/security_compartments.csv') as f:
		data = csv.DictReader(f)
		for r in data:
			outf.write("INSERT INTO sec_compartments (abbrv,comment) VALUES ('%s','%s');\n"%(r['compartment_tag'],r['compartment_desc']))


########################################
# FACILITY & INVENTORY DATA PROCESSING #
########################################
def facilities():
	# Empty Facilities
	insert("facilities", ["fcode", "common_name", "location"], ["S300", "Site 300", "UNDISCLOSED"])
	insert("facilities", ["fcode", "common_name", "location"], ["GRLK", "Groom Lake, Nevada", "Groom Lake, NV"])
	insert("facilities", ["fcode", "common_name", "location"], ["GRLK", "Los Alamos, New Mexico", "Los Alamos, NM"])

	# Facilities With Inventory
	for fn in glob.iglob('./osnap_legacy/**/*.csv', recursive=True):
		if "inventory" in fn:
			fcode = fn.split('/')[2].split('_')[0]

			# Translate facility code into understandable data
			if fcode == "HQ":
				common_name = "Headquarters"
				location = "Eugene, OR"
			elif fcode == "DC":
				common_name = "The Capitol"
				location = "Washington, D.C."
			elif fcode == "SPNV":
				common_name = "Sparks, Nevada"
				location = "Sparks, NV"
			elif fcode == "NC":
				common_name = "National City"
				location = "National City, CA"
			elif fcode == "MB005":
				common_name = "Moonbase"
				location = "Earth's Moon"

			insert("facilities", ["fcode", "common_name", "location"], [fcode, common_name, location])
			CUR.execute("SELECT facility_pk FROM facilities WHERE fcode = '" + fcode + "';")
			facility_pk = CUR.fetchone()[0]
			inventory(fn, facility_pk)

def inventory(fn, facility_fk):
	reader = csv.reader(open(fn, newline=''), delimiter=',', quotechar='|')
	head = next(reader)
	for row in reader:
		insert("assets", ["asset_tag", "description"], [row[0], row[2]])
		CUR.execute("SELECT asset_pk FROM assets WHERE asset_tag = '" + row[0] + "';")
		asset_fk = CUR.fetchone()[0]
		insert("asset_at", ["asset_fk", "facility_fk"], [asset_fk, facility_fk])

################
# PRODUCT DATA #
################
def process_products(outf):
	with open('osnap_legacy/product_list.csv') as f:
		data = csv.DictReader(f)
		for r in data:
			for k in r.keys():
				print("%s: %s" % (k, r[k]))
				if r[k] == '':
					r[k] = 'NULL'
				elif k == 'unit price':
					pass
				else:
					r[k] = "'%s'" % r[k]  # if single quotes are in the data this will fail

			# Add the product entry
			outf.write("INSERT INTO products (vendor,product_name,product_model,description,price) VALUES (%s,%s,%s,%s,%s);\n" % (
			r['vendor'], r['name'], r['model'], r['description'], r['unit price']))

			# Add the security tag if there is one
			if not r['compartments'] == 'NULL':
				(tc, tl) = r['compartments'].split(':')

			'''
			This query exploits how serial values are generated and may fail
			if something else is running at the same time as the migration script.
			This query is also likely to be super inefficient for large migrations.
			'''
			outf.write("INSERT INTO security_tags (level_fk, compartment_fk, product_fk) "
					   "SELECT level_pk, compartment_pk, max(product_pk) FROM sec_levels l,sec_compartments c,products p "
					   "WHERE l.abbrv='%s and c.abbrv=%s' GROUP BY level_pk,compartment_pk,product_pk;\n" % (tl, tc))


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
	CUR.execute(sql_insert)


if __name__ == '__main__':
	global DB_NAME
	global PORT
	global CUR

	try:
		DB_NAME = sys.argv[1]
		PORT = int(sys.argv[2])
		print("\nDATABASE AND PORT ARE CORRECT! Connecting to lost:5432...\n")

	except:
		print("\nError with command line arguments!\nConnecting to lost:5432 anyways...\n")
		DB_NAME = 'lost'
		PORT = '5432'

		# Connect to database
		conn = "host='localhost' port='" + PORT + "' dbname='" + DB_NAME + "' user='osnapdev' password='secret'"
		print("Connecting to database\n ->%s" % conn)
		db = psycopg2.connect(conn)
		print("CONNECTION COMPLETE")

		# Instantiate database cursor
		CUR = db.cursor()

		# Increase work memory
		work_mem = 1024
		CUR.execute('SET work_mem TO ' + str(work_mem))

	else:
		# Connect to database
		conn = "host='localhost' port='" + PORT + "' dbname='" + DB_NAME + "' user='osnapdev' password='secret'"
		print("Connecting to database\n ->%s" % conn)
		db = psycopg2.connect(conn)
		print("CONNECTION COMPLETE")

		# Instantiate database cursor
		CUR = db.cursor()

		# Increase work memory
		work_mem = 1024
		CUR.execute('SET work_mem TO ' + str(work_mem))

	main()
