from flask import request, flash, render_template
import bcrypt

from app import app, helpers


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username', None).strip()  # Aa09_.- allowed
        password = request.form.get('password', None)
        role = request.form.get('role', 'Guest')

        if re.match(r'^[\w.-]+$', username) and password:
            # Form was completed with valid input
            matching_user = "SELECT user_pk FROM users WHERE username = %s;"
            user_does_exist = helpers.duplicate_check(matching_user, [username])

            if user_does_exist:
                flash('Username already exists')
            else:
                salt = bcrypt.gensalt(12)
                password = bcrypt.hashpw(password.encode('utf-8'), bytes(salt))
                new_user = ("INSERT INTO users (username, password, salt, role_fk) "
                            "VALUES (%s, %s, %s, %s);")
                helpers.db_change(new_user, [username, password, salt, role])
                flash('Your account was created!')

        else:
            flash('Please enter a username and password.')

    return render_template('create_user.html')
