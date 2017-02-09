from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2, sys, os, datetime

from config import *


# Instantiate App
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# Database Query Function
def db_query(sql_string, data_array):
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	print("\nIn db_query('" + sql_string + "',", data_array, "):\n")
	cur.execute(sql_string, data_array)

	# Return data as a dictionary
	result = cur.fetchall()
	if len(result) != 0:
		entries = result
		records = []
		for row in entries:
			records.append(row)
			print("\n\n\nCurrently in row:", row)
		print("\n\n Records list is:", records)
	else:
		print("\n\n NO RESULTS FOR QUERY \n\n")
		records = None

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
		raise ValueError("Incorrect data format, should be MM/DD/YYYY")


# Templates
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if False and request.form['username'] != USERNAME:
			error = 'Invalid username'
		elif False and request.form['password'] != PASSWORD:
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


# TODO: Learn difference between redirect and render functions (lines 115 and 128)
# TODO: Learn how to properly utilize the 'sessions' module


@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
	# Get facilities list for drop-down menu
	# I don't use the db_query function here because there's no data argument
	fac_query = 'SELECT common_name FROM facilities;'
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	cur.execute(fac_query)
	list_of_single_tuples = cur.fetchall()
	facilities_list = []
	for item in list_of_single_tuples:
		facilities_list.append(item[0])
	print("\n\n", facilities_list, "\n\n")
	conn.commit()
	cur.close()
	conn.close()

	# If a form has been submitted
	if request.method == 'POST':
		# Validate and pass date
		try:
			validated_date = validate_date(request.form['filter_date'])
		except ValueError:
			print("\n\nValueError.args is:", ValueError.args, "\n\n")
			flash(ValueError.args)
		except TypeError or UnboundLocalError:
			flash("You need to enter a date.")

		# Filtering Inventory by whether or not it is "In Transit"
		if request.form['filter_facility'] == 'none':
			moving_query = "SELECT assets.asset_tag, assets.description, f1.location as location1, f2.location as location2, convoys.depart_dt, convoys.arrive_dt" \
						   " FROM assets" \
						   " JOIN asset_on ON assets.asset_pk = asset_on.asset_fk" \
						   " JOIN convoys ON asset_on.convoy_fk = convoys.convoy_pk" \
						   " JOIN facilities f1 ON convoys.src_fk = f1.facility_pk" \
						   " JOIN facilities f2 ON convoys.dst_fk = f2.facility_pk" \
						   " WHERE convoys.arrive_dt >= %s AND convoys.depart_dt <= %s"

			moving_inventory_data = db_query(moving_query, [validated_date, validated_date])
			print("Data being sent via render is:", moving_inventory_data)
			if moving_inventory_data is not None:
				for record in moving_inventory_data:
					print("This is the record being iterated over the returned data:", record)
			else:
				moving_inventory_data = []

			return render_template('moving_inventory.html', date=validated_date, data=moving_inventory_data)

		# Filtering Inventory by Facility
		else:
			selected_facility = str(request.form['filter_facility'])
			facility_query = "SELECT facilities.fcode, facilities.location, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt" \
							 " FROM facilities" \
							 " JOIN asset_at ON facilities.facility_pk = asset_at.facility_fk" \
							 " JOIN assets ON asset_at.asset_fk = assets.asset_pk" \
							 " WHERE facilities.common_name = %s" \
							 " AND asset_at.arrive_dt >= %s AND asset_at.depart_dt >= %s;"

			facility_inventory_data = db_query(facility_query, [selected_facility, validated_date, validated_date])
			if facility_inventory_data is None:
				facility_inventory_data = []
			return render_template('facility_inventory.html', facility=selected_facility, data=facility_inventory_data, date=validated_date)

	return render_template('report_filter.html', facilities_list=facilities_list)


@app.route('/facility_inventory', methods=['GET', 'POST'])
def facility_inventory():
	return render_template('facility_inventory.html', facility=request.args.get('facility'), date=request.args.get('report_date'))


@app.route('/moving_inventory', methods=['GET', 'POST'])
def moving_inventory():
	return render_template('moving_inventory.html', date=request.args.get('report_date'))


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# TODO: Implement other error handlers - http://flask.pocoo.org/docs/0.12/patterns/errorpages/


# Application Deployment
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)