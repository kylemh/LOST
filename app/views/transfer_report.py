from flask import render_template

from app import app


# TODO: Implement View
@app.route('/transfer_report', methods=['GET', 'POST'])
def transfer_report():
    return render_template('transfer_report.html')
