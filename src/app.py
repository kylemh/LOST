"""
TODO: Implement other error handlers - http://flask.pocoo.org/docs/0.12/patterns/errorpages/
TODO: Shit-loads of refactoring
TODO: Proper Error Handling of Entries in report_filter()
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import datetime

from config import *


# Instantiate App
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# MARK: DATABASE FUNCTIONS
# Database Query Function
def db_query(sql_string, data_array):
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	cur.execute(sql_string, data_array)
	print('Query being executed:', sql_string)

	# Return data as an array of dictionaries
	result = cur.fetchall()
	print('Query result:', result)
	records = []

	# If the query returns something...
	if len(result) != 0:
		entries = result
		print("\nLine 33 - entries:", entries)
		for row in entries:
			records.append(row)
	else:
		# No results in query
		print('\n\bNO RESULTS IN QUERY\n')
		redirect(url_for('failed_query', query_string=sql_string))

	conn.commit()
	cur.close()
	conn.close()
	return records


# Date Validation Function
def validate_date(date_string):
	try:
		date = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
		return str(date)
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
				   ' WHERE convoys.arrive_dt >= %s AND convoys.depart_dt <= %s'

	moving_inventory_data = db_query(moving_query, [validated_date, validated_date])

	column_names = ['asset_tag', 'description', 'location1', 'location2', 'depart_dt', 'arrive_dt']
	moving_inventory_processed = []

	# TODO: Refactor by creating array of tuples to dictionary conversion function
	# If list is not empty and it's size matches the array of column headers
	if moving_inventory_data and (len(moving_inventory_data[0]) == len(column_names)):
		for record in moving_inventory_data:
			moving_inventory_processed.append(dict(zip(column_names, record)))
	else:
		print('\n\nERROR LIST OF COLUMN SIZE IS NOT THE SAME SIZE AS RECORD SIZE\n\n')

	return render_template('moving_inventory.html', date=validated_date, data=moving_inventory_processed)


@app.route('/facility_inventory', methods=['GET', 'POST'])
def facility_inventory(validated_date):
	selected_facility = str(request.form['filter_facility'])
	facility_query = 'SELECT facilities.fcode, facilities.location, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt' \
					 ' FROM (SELECT * FROM facilities WHERE common_name = %s) as facilities' \
					 ' JOIN asset_at ON facilities.facility_pk = asset_at.facility_fk' \
					 ' JOIN assets ON asset_at.asset_fk = assets.asset_pk' \
					 ' WHERE (asset_at.depart_dt <= %s OR asset_at.depart_dt IS NULL)' \
					 ' AND asset_at.arrive_dt >= %s;'

	facility_inventory_data = db_query(facility_query, [selected_facility, validated_date, validated_date])
	print("\n\nLine 166 - facility_inventory_data:\n", facility_inventory_data)


	column_names = ['fcode', 'location', 'asset_tag', 'description', 'arrive_dt', ' depart_dt']
	facility_inventory_processed = []

	# TODO: Refactor by creating array of tuples to dictionary conversion function
	# If list is not empty and it's size matches the array of column headers
	if facility_inventory_data and (len(facility_inventory_data[0]) == len(column_names)):
		for record in facility_inventory_data:
			facility_inventory_processed.append(dict(zip(column_names, record)))
	else:
		print('\n\nERROR LIST OF COLUMN SIZE IS NOT THE SAME SIZE AS RECORD SIZE\n\n')

	print('\nThis is the data being passed:', facility_inventory_processed)
	return render_template('facility_inventory.html', facility=selected_facility, data=facility_inventory_processed, date=validated_date)


@app.route('/facility_inventory', methods=['GET'])
def failed_query(query_string):
	return render_template('failed_query.html', query=query_string)


# MARK: ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Application Deployment
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)