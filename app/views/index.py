from flask import redirect, url_for

from app import app


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return redirect(url_for('login'))
