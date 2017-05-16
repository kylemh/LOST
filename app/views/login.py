from flask import render_template, request, redirect, url_for, session, flash

from app import app, helpers


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

        # Login form is not blank.
        check_for_user = "SELECT * FROM users WHERE username = %s;"
        result = helpers.db_query(check_for_user, [username])

        # User does not exist.
        if result is None:
            flash('There is no record of this account.')
            return render_template('login.html')

        # User is deactivated.
        if not result[0][4]:
            flash('This account has been deactivated')
            return render_template('login.html')

        # User exists:
        authorized = helpers.authorize(username, password)

        # Password is correct
        if authorized:
            session['username'] = username
            session['logged_in'] = True
            session['perms'] = result[0][1]
            session['user_id'] = result[0][0]
            return redirect('/dashboard')

        # Password is incorrect
        else:
            flash('Password is incorrect.')

    return render_template('login.html')
