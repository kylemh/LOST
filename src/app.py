from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import sys, psycopg2

from src.config import HOST, PORT, DEBUG, APP_SECRET_KEY, DB_LOCATION

app = Flask(__name__)
app.secret_key = str(APP_SECRET_KEY)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/report_menu')
def report_menu():
	# cur.execute("SELECT * FROM assets")
	# records = cur.fetchall()
	# processed_data = []
	# for r in res:
	# 	processed_data.append( dict(zip(('asset_tag', 'description'), r)))
	# return render_template('report_menu.html', processed_data=processed_data)
	return render_template('report_menu.html')


@app.route('/report_filter')
def report_filter():
	return render_template('report_filter.html')


@app.route('/facility_inventory')
def facility_inventory_report():
	return render_template('facility_inventory.html', facility=request.args.get('facility'), date=request.args.get('report_date'))


@app.route('/moving_inventory')
def in_transit_report():
	return render_template('moving_inventory.html', date=request.args.get('report_date'))


@app.route('/logout')
def logout():
	return render_template('logout.html')


# if __name__ == "__main__":
# 	app.run(host = config.DB_LOCATION, port = config.PORT, debug = config.DEBUG)
