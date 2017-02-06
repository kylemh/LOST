from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2, sys, os, datetime

from config import *


# Instantiate App
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# Database Query Function
def db_query(sql_string, for_selection, passed_data):
	conn = psycopg2.connect(DB_LOCATION)
	cur = conn.cursor()
	print("The query being executed is", sql_string, "\n")
	if passed_data is None:
		cur.execute(sql_string)
	else:
		cur.execute(sql_string, passed_data)

	if for_selection is True:
		try:
			entries = cur.fetchall()
			data = []
			for row in entries:
				for column in row:
					data.append(column)
		except:
			data = ''
	else:
		try:
			entries = cur.fetchall()
			data = {}
			for row in entries:
				for column in row:
					data[column] = row
		except:
			data = ''

	conn.commit()
	cur.close()
	conn.close()
	return data


# Date Validation Function
def validate_date(date_string):
	try:
		date = datetime.datetime.strptime(date_string, '%m/%d/%Y')
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


@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
	# Get facilities list for drop-down menu
	facilities_list = db_query('SELECT common_name FROM facilities;', True, None)

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

		# Not filtering by facility...
		if request.form['filter_facility'] == 'none':
			moving_query = "SELECT assets.asset_tag, assets.description, f1.location as 'location1', f2.location as 'location2', convoys.arrive_dt, convoys.depart_dt" \
						   "FROM assets" \
						   "JOIN asset_on ON assets.asset_pk = asset_on.asset_fk" \
						   "JOIN convoy ON asset_fk" \
						   "JOIN facilities f1 ON convoy.src_fk = f1.facility_pk" \
						   "JOIN facilities f2 ON convoy.dst_fk = f2.facility_pk" \
						   "WHERE convoys.arrive_dt >= %d AND convoys.depart_dt <= %d"

			moving_inventory_data = db_query(moving_query, for_selection=False, passed_data=validated_date)
			return redirect(url_for('moving_inventory'), date=validated_date, data=moving_inventory_data)

		# Filtering by facility...
		else:
			selected_facility = request.form['filter_facility']
			facility_query = "SELECT facilities.fcode, facilities.location, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt" \
							 "FROM facilities" \
							 "JOIN asset_at ON facilities.facility_pk = asset_at.facility_fk" \
							 "JOIN assets ON asset_at.asset_fk = assets.asset_pk" \
							 "WHERE facilities.common_name = ''' + facility + "'' \
							 "AND asset_at.arrive_dt >= %d AND asset_at.depart_dt <= %d;"

			facility_inventory_data = db_query(facility_query, for_selection=False, passed_data=validated_date)
			return redirect(url_for('facility_inventory'), facility=selected_facility, data=facility_inventory_data)

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