from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2, sys, os

from config import *


# Instantiate App
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

# Database Connection
CONN = psycopg2.connect(DB_LOCATION)
CUR = CONN.cursor()


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


@app.route('/report_filter')
def report_filter():
	return render_template('report_filter.html')


@app.route('/facility_inventory')
def facility_inventory():
	return render_template('facility_inventory.html', facility=request.args.get('facility'), date=request.args.get('report_date'))


@app.route('/moving_inventory')
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
