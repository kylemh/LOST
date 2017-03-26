from flask import redirect, url_for
import app

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return redirect(url_for('login'))