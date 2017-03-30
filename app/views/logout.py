from flask import session, render_template

from app import app


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('logout.html')
