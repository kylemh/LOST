from flask import Flask, render_template, request
from config import DB_NAME, HOST, PORT, DB_LOCATION, DEBUG
import sys
import psycopg2


app = Flask(__name__)

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

@app.route('/facility_inventory_report')
def facility_inventory_report():
	return render_template('facility_inventory_report.html',facility=request.args.get('facility'),date=request.args.get('report_date'))

@app.route('/in_transit_report')
def in_transit_report():
	return render_template('in_transit_report.html',date=request.args.get('report_date'))

@app.route('/logout')
def logout():
	return render_template('logout.html')

# if __name__ == "__main__":
# 	app.run(host='0.0.0.0',port=8080)