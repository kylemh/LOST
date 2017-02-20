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
	"""This function is designed to take a SQL query string and a list of data to be used (in order) as injection-safe, variable fill-ins for the query."""
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
	except e:
		print("INSERTION FAILED")

	conn.commit()
	cur.close()
	conn.close()


# MARK: TEMPLATES
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if session['logged_in'] == True:
		return redirect(url_for('dashboard'))

	error = None
	if request.method == 'POST':
		username = request.form.get('username', None)
		password = request.form.get('password', None)

		if username is None:
			error = 'Please enter a username.'
		elif password is None:
			error = 'Please enter a password.'
		else:
			check_for_user = "SELECT * FROM users WHERE username = %s;"
			result = db_query(check_for_user, [username])

			if result is None:
				# User DOES NOT exist:
				error = 'There is no record of this account.'
			else:
				# User DOES exist:
				if password == result[0][2]:
					# Password is correct
					session['username'] = username
					session['logged_in'] = True
					flash('Welcome', username)
					return redirect('/dashboard')
				else:
					# Password is incorrect
					error = 'Password is incorrect.'

	return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['logged_in'] = False
	return render_template('logout.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
	if session['logged_in'] == False:
		return redirect(url_for('login'))
	else:
		return render_template('dashboard.html')


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == 'POST':
		if 'arguments' in request.form:
			user_request = json.loads(request.form['arguments'])
			username = user_request['username']
			password = user_request['password']
		else:
			username = request.form['username']
			password = request.form['password']

		check_for_username = "SELECT user_pk FROM users WHERE username = %s;"
		response = db_query(check_for_username, [username])

		if response is not None:
			flash('Username already exists')
		else:
			add_username = "INSERT INTO users (username, password) VALUES (%s, %s);"
			db_insert(add_username, [username, password])
			flash('Your account was created!')

	return render_template('create_user.html')


@app.route('/failed_query', methods=['GET'])
def failed_query(query_string):
	return render_template('failed_query.html', query=query_string)


# MARK: ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# Application Deployment
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
