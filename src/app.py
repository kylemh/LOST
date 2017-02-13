"""
TODO: Implement other error handlers - http://flask.pocoo.org/docs/0.12/patterns/errorpages/
TODO: Shit-loads of refactoring
TODO: Proper Error Handling of Entries in report_filter()
TODO: Implement logout.html
TODO: Add button to point to rest.html on login page
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import datetime

from config import *


# Instantiate App
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# MARK: DATABASE FUNCTIONS
def db_query(sql_string, data_array):
	"""This function is designed to take SQL query and a list of data to be used (in order) as variable fill-ins for the query."""
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	cur.execute(sql_string, data_array)

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
		print('\nNO RESULTS IN QUERY\n')
		# TODO: Redirect to to failed_query.html

	conn.commit()
	cur.close()
	conn.close()
	return records


def validate_date(date_string):
	"""This function checks to see if the user entered a date in the MM/DD/YYYY format."""
	try:
		date = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
		return date
	except ValueError:
		raise ValueError('Incorrect data format, should be MM/DD/YYYY')


# MARK: TEMPLATES
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if False or request.form['username'] != USERNAME:
			error = 'Invalid username'
		elif False or request.form['password'] != PASSWORD:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			session['username'] = request.form['username']
			session['password'] = request.form['password']
			return redirect(url_for('report_filter'))

	return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['logged_in'] = False
	return render_template('logout.html')


@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
	# Populate Facilities Drop-down menu
	fac_query = 'SELECT common_name FROM facilities;'
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	cur.execute(fac_query)
	list_of_single_tuples = cur.fetchall()

	facilities_list = []
	for name, in list_of_single_tuples:
		facilities_list.append(name)

	conn.commit()
	cur.close()
	conn.close()

	# If a form has been submitted
	if request.method == 'POST':
		# Validate and pass date
		try:
			validated_date = validate_date(request.form['filter_date'])
		except ValueError:
			print('VALUE ERROR:', ValueError.args)
			pass
		except TypeError or UnboundLocalError:
			print('TYPE ERROR:', 'You need to enter a date.')
			pass

		# FILTER: Inventory by 'In Transit' status
		if request.form['filter_facility'] == 'none':
			return moving_inventory(validated_date)

		# FILTER: Inventory by Facility
		else:
			return facility_inventory(validated_date)

	return render_template('report_filter.html', facilities_list=facilities_list)


@app.route('/moving_inventory', methods=['GET', 'POST'])
def moving_inventory(validated_date):
	moving_query = 'SELECT assets.asset_tag, assets.description, f1.location as location1, f2.location as location2, convoys.depart_dt, convoys.arrive_dt' \
				   ' FROM assets' \
				   ' JOIN asset_on ON assets.asset_pk = asset_on.asset_fk' \
				   ' JOIN convoys ON asset_on.convoy_fk = convoys.convoy_pk' \
				   ' JOIN facilities f1 ON convoys.src_fk = f1.facility_pk' \
				   ' JOIN facilities f2 ON convoys.dst_fk = f2.facility_pk' \
				   ' WHERE convoys.arrive_dt >= %s AND convoys.depart_dt <= %s;'

	moving_inventory_data = db_query(moving_query, [validated_date, validated_date])

	column_names = ['asset_tag', 'description', 'location1', 'location2', 'depart_dt', 'arrive_dt']
	moving_inventory_processed = []

	# TODO: Refactor by creating array of tuples to dictionary conversion function
	# If list is not empty and it's size matches the array of column headers
	if moving_inventory_data and (len(moving_inventory_data[0]) == len(column_names)):
		for record in moving_inventory_data:
			moving_inventory_processed.append(dict(zip(column_names, record)))
	else:
		print('\n\nERROR - LIST OF COLUMN SIZE IS NOT THE SAME SIZE AS RECORD SIZE\n\n')

	return render_template('moving_inventory.html', date=validated_date, data=moving_inventory_processed)


@app.route('/facility_inventory', methods=['GET', 'POST'])
def facility_inventory(validated_date):
	selected_facility = request.form['filter_facility']
	facility_query = 'SELECT facilities.fcode, facilities.location, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt' \
					 ' FROM (SELECT * FROM facilities WHERE common_name = %s) as facilities' \
					 ' JOIN asset_at ON facilities.facility_pk = asset_at.facility_fk' \
					 ' JOIN assets ON asset_at.asset_fk = assets.asset_pk' \
					 ' WHERE (asset_at.depart_dt >= %s OR asset_at.depart_dt IS NULL)' \
					 ' AND asset_at.arrive_dt <= %s;'

	facility_inventory_data = db_query(facility_query, [selected_facility, validated_date, validated_date])

	column_names = ['fcode', 'location', 'asset_tag', 'description', 'arrive_dt', ' depart_dt']
	facility_inventory_processed = []

	# TODO: Refactor by creating array of tuples to dictionary conversion function
	# If list is not empty and it's size matches the array of column headers
	if facility_inventory_data and (len(facility_inventory_data[0]) == len(column_names)):
		for record in facility_inventory_data:
			facility_inventory_processed.append(dict(zip(column_names, record)))
	else:
		print('\n\nERROR - LIST OF COLUMN SIZE IS NOT THE SAME SIZE AS RECORD SIZE\n\n')

	return render_template('facility_inventory.html', facility=str(selected_facility), data=facility_inventory_processed, date=validated_date)


@app.route('/facility_inventory', methods=['GET'])
def failed_query(query_string):
	return render_template('failed_query.html', query=query_string)


# MARK: ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# MARK: REST API
@app.route('/rest')
def rest():
	return render_template('rest.html')


@app.route('/rest/lost_key', methods=['POST'])
def lost_key():
	json_data = dict()
	json_data['timestamp'] = str(datetime.datetime.now())
	json_data['result'] = 'OK'
	json_data['key'] = 'bksaoudu......aoelchsauh'
	data = json.dumps(json_data)
	return data


@app.route('/rest/activate_user', methods=['POST'])
def activate_user():
	if request.method == 'POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
		json_data = dict()
		json_data['timestamp'] = req['timestamp']
		json_data['result'] = 'OK'
		data = json.dumps(json_data)
		return data
	else:
		return redirect(url_for('rest'))


@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
	if request.method == 'POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
		json_data = dict()
		json_data['timestamp'] = req['timestamp']

		conn = psycopg2.connect(DB_LOCATION)
		cur = conn.cursor()

		try:
			cur.execute("INSERT INTO users (username) VALUES ('" + req['username'] + "');")
			conn.commit()
			json_data['result'] = 'OK'
		except Exception as e:
			json_data['result'] = 'FAIL'

		conn.close()
		data = json.dumps(json_data)
		return data

	else:
		return redirect(url_for('rest'))


@app.route('/rest/list_products', methods=('POST',))
def list_products():
	# Provided Function
	if request.method == 'POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
	else:
		return redirect(url_for('rest'))

	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()

	if len(req['compartments']) == 0:
		print("\nDO NOT HAVE COMPARTMENT PERMISSIONS\n")
		listing_query = "SELECT vendor, description, string_agg(c.abbrv||':'||l.abbrv,',') " \
				   "FROM products p " \
				   "LEFT JOIN security_tags t ON p.product_pk = t.product_fk " \
				   "LEFT JOIN sec_compartments c ON t.compartment_fk = c.compartment_pk " \
				   "LEFT JOIN sec_levels l ON t.level_fk = l.level_pk"

		if req['vendor'] == '' and req['description'] == '':
			listing_query += " GROUP BY vendor, description"
			cur.execute(listing_query)
		else:
			if not req['vendor'] == '' and not req['description'] == '':
				req['vendor'] = "%" + req['vendor'] + "%"
				req['description'] = "%" + req['description'] + "%"
				listing_query += " WHERE description ilike %s AND vendor ilike %s GROUP BY vendor, description"
				cur.execute(listing_query, (req['description'], req['vendor']))
			elif req['vendor'] == '':
				req['description'] = "%" + req['description'] + "%"
				listing_query += " WHERE description ilike %s GROUP BY vendor, description"
				cur.execute(listing_query, (req['description'],))
			elif req['description'] == '':
				req['vendor'] = "%" + req['vendor'] + "%"
				listing_query += " WHERE vendor ilike %s GROUP BY vendor, description"
				cur.execute(listing_query, (req['vendor'],))
	else:
		print("You have compartment %s" % len(req['compartments']))
		listing_query = "SELECT vendor, description, string_agg(c.abbrv||':'||l.abbrv,',') " \
				   "FROM security_tags t " \
				   "LEFT JOIN sec_compartments c ON t.compartment_fk = c.compartment_pk " \
				   "LEFT JOIN sec_levels l ON t.level_fk = l.level_pk " \
				   "LEFT JOIN products p ON t.product_fk = p.product_pk " \
				   "WHERE product_fk IS NOT NULL " \
				   "AND c.abbrv||':'||l.abbrv = ANY(%s)"

		if req['vendor'] == '' and req['description'] == '':
			listing_query += " GROUP BY vendor, description, product_fk HAVING count(*) = %s"
			cur.execute(listing_query, (req['compartments'], len(req['compartments'])))
		else:
			if not req['vendor'] == " AND NOT req['description'] == ":
				req['vendor'] = "%" + req['vendor'] + "%"
				req['description'] = "%" + req['description'] + "%"
				listing_query += " AND description ilike %s AND vendor ilike %s GROUP BY vendor, description, product_fk HAVING count(*) = %s"
				cur.execute(listing_query, (req['compartments'], req['description'], req['vendor'], len(req['compartments'])))
			elif req['vendor'] == '':
				req['description'] = "%" + req['description'] + "%"
				listing_query += " AND description ilike %s GROUP BY vendor, description, product_fk HAVING count(*) = %s"
				cur.execute(listing_query, (req['compartments'], req['description'], len(req['compartments'])))
			elif req['description'] == '':
				req['vendor'] = "%" + req['vendor'] + "%"
				listing_query += " AND vendor ilike %s GROUP BY vendor, description, product_fk HAVING count(*) = %s"
				cur.execute(listing_query, (req['compartments'], req['vendor'], len(req['compartments'])))

	dbres = cur.fetchall()
	listing = list()
	for row in dbres:
		e = dict()
		e['vendor'] = row[0]
		e['description'] = row[1]
		if row[2] is None:
			e['compartments'] = list()
		else:
			e['compartments'] = row[2].split(',')
		listing.append(e)

	# Prepare the response
	json_data = dict()
	json_data['timestamp'] = req['timestamp']
	json_data['listing'] = listing
	data = json.dumps(json_data)

	# TODO: See if you can move the connection closer higher up
	conn.close()

	return data


@app.route('/rest/add_products', methods=['POST'])
def add_products():
	if request.method == 'POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
		json_data = dict()
		json_data['timestamp'] = req['timestamp']

		conn = psycopg2.connect(DB_LOCATION)
		cur = conn.cursor()

		try:
			cur.execute("INSERT INTO products (description, vendor) VALUES ('" + "description" + "', 'vendor');")
			conn.commit()
			json_data['result'] = 'OK'
		except Exception as e:
			json_data['result'] = 'FAIL'

		conn.close()
		data = json.dumps(json_data)
		return data

	else:
		return redirect(url_for('rest'))

@app.route('/rest/add_asset', methods=['POST'])
def add_asset():
	if request.method == 'POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
		json_data = dict()
		json_data['timestamp'] = req['timestamp']

		conn = psycopg2.connect(DB_LOCATION)
		cur = conn.cursor()

		try:
			cur.execute("INSERT INTO assets (description) VALUES ('" + req['description'] + "');")
			conn.commit()
			json_data['result'] = 'OK'
		except Exception as e:
			json_data['result'] = 'FAIL'

		conn.close()
		data = json.dumps(json_data)
		return data

	else:
		return redirect(url_for('rest'))


# Application Deployment
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
