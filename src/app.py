"""
TODO: Implement other error handlers - http://flask.pocoo.org/docs/0.12/patterns/errorpages/
TODO: Shit-loads of refactoring
TODO: Proper Error Handling of Entries in report_filter()
TODO: Implement logout.html
TODO: Add button to point to rest.html on login page
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2, json

from config import DB_NAME, HOST, PORT, APP_SECRET_KEY


# Run Server
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# MARK: DATABASE FUNCTIONS
def db_query(sql_string, data_list):
	"""This function is designed to take a SQL query string and a list of data to be used - in order - as injection-safe, variable fill-ins for the query."""
	conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
	cur = conn.cursor()
	cur.execute(sql_string, data_list)

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
		return None

	conn.commit()
	cur.close()
	conn.close()
	return records


def db_insert(sql_string, data_list):
	"""This function is designed to take a SQL query string and a list of data to be used (in order) as injection-safe, variable fill-ins for the query."""
	conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
	cur = conn.cursor()
	try:
		cur.execute(sql_string, data_list)
	except:
		print("INSERTION FAILED")

	conn.commit()
	cur.close()
	conn.close()


def duplicate_check(sql_string, data_list):
	"""This function is designed to return True if a query yields a result and False if not."""
	conn = psycopg2.connect(dbname=DB_NAME, host=HOST, port=PORT)
	cur = conn.cursor()
	cur.execute(sql_string, data_list)
	result = cur.fetchall()
	cur.close()
	conn.close()
	if result:
		return True
	else:
		return False


# MARK: TEMPLATES
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get('logged_in'):
		return redirect(url_for('dashboard'))

	if request.method == 'POST':
		username = request.form.get('username', None)
		password = request.form.get('password', None)

		if username is None:
			flash('Please enter a username.')
			return render_template('login.html')
		elif password is None:
			flash('Please enter a password.')
			return render_template('login.html')
		else:
			check_for_user = "SELECT * FROM users WHERE username = %s;"
			result = db_query(check_for_user, [username])
			# Result is ([user_pk, role_fk, username, password])

			if result is None:
				# User DOES NOT exist:
				flash('There is no record of this account.')
				return render_template('login.html')
			else:
				# User DOES exist:
				if password == result[0][3]:
					# Password is correct
					session['username'] = username
					session['logged_in'] = True
					session['perms'] = result[0][1]
					welcome_message = 'Welcome ' + str(session.get('username')) + '!'
					flash(welcome_message)
					return redirect('/dashboard')
				else:
					# Password is incorrect
					flash('Password is incorrect.')
					return render_template('login.html')

	return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['logged_in'] = False
	return render_template('logout.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
	if not session.get('logged_in'):
		flash('You must login before being allowed access to the dashboard')
		return redirect(url_for('login'))
	else:
		return render_template('dashboard.html')


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == 'POST':
		username = request.form.get('username', None)
		password = request.form.get('password', None)
		role = request.form.get('role', 'Guest')

		if username is None:
			flash('Please enter a username.')
		elif password is None:
			flash('Please enter a password.')
		else:
			# Form was completed
			matching_user = "SELECT user_pk FROM users WHERE username = %s;"
			user_does_exist = duplicate_check(matching_user, [username])

			if user_does_exist:
				flash('Username already exists')
			else:
				# User does not already exist - create it
				new_user = "INSERT INTO users (username, password, role_fk) VALUES (%s, %s, %s);"
				db_insert(new_user, [username, password, role])
				flash('Your account was created!')

	return render_template('create_user.html')


@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
	if request.method == 'POST':
		fcode = request.form.get('fcode', None)
		common = request.form.get('common', None)
		location = request.form.get('location', None)

		if fcode is None or common is None or location is None:
			flash('Please complete the form')
		else:
			matching_facilities = "SELECT facility_pk FROM facilities WHERE fcode=%s OR common_name=%s;"
			facility_does_exist = duplicate_check(matching_facilities, [fcode, common])

			if facility_does_exist:
				flash('There already exists a facility with that fcode or common name!')
			else:
				# Facility does not already exist - create it
				new_facility = "INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);"
				db_insert(new_facility, [fcode, common, location])
				flash('New facility was created!')

	# Get all current facilities for table population
	all_facilities = "SELECT * FROM facilities;"
	data = db_query(all_facilities, [])
	print(data)

	return render_template('add_facility.html', data=data)


# MARK: ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.route('/failed_query', methods=['GET'])
def failed_query(query_string):
	return render_template('failed_query.html', query=query_string)


# Application Deployment
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
