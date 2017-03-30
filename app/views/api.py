from flask import request, json

from app import app, helpers


@app.route('/rest/activate_user', methods=['POST'])
def activate_user():
    if request.method == 'POST' and 'arguments' in request.form:
        api_req = json.loads(request.form['arguments'])

        # If http request is missing a parameter...
        if 'username' not in api_req or 'password' not in api_req or 'role' not in api_req:
            error_result = json.dumps({'result': 'Error: Missing Parameters'})
            return error_result
        else:
            username = api_req['username']
            password = api_req['password']
            role = api_req['role']

        # Handle errors within CLI arguments.
        if len(username) > 16 or len(password) > 16:
            error_result = json.dumps({'result': 'Error: Username or Password Too Long'})
            return error_result

        # All parameters are valid.
        if role == 'logofc':
            role = 2
        elif role == 'facofc':  # facofc
            role = 3
        else:
            error_result = json.dumps({'result': 'Error: Unsupported Role'})
            return error_result

        matching_user = "SELECT * FROM users WHERE username = %s"
        user_does_exist = helpers.db_query(matching_user, [username])

        # If user exists in database, activate user; otherwise, create and activate new user.
        if user_does_exist:
            activate_existing_user = ("UPDATE users SET password = %s, active = TRUE "
                                      "WHERE username = %s")
            helpers.db_change(activate_existing_user, [password, username])
        else:
            create_user = ("INSERT INTO users (user_pk, role_fk, username, password, active) "
                           "VALUES (DEFAULT, %s, %s, %s, TRUE)")
            helpers.db_change(create_user, [role, username, password])

        data = json.dumps({'result': 'OK'})
        return data


@app.route('/rest/revoke_user', methods=['POST'])
def revoke_user():
    if request.method == 'POST' and 'arguments' in request.form:
        api_req = json.loads(request.form['arguments'])
        print('This is the api_req', api_req)

        # If http request is missing a parameter...
        if 'username' not in api_req:
            error_result = json.dumps({'result': 'Error: Missing Parameter(s)'})
            return error_result

        # All parameters present in request.
        username = api_req['username']

        matching_user = "SELECT * FROM users WHERE username = %s"
        user_does_exist = helpers.db_query(matching_user, [username])

        # If user exists in database, deactivate user; otherwise, return "User Not Found" API Error.
        if user_does_exist:
            deactivate_existing_user = ("UPDATE users SET active = FALSE "
                                        "WHERE username = %s")
            helpers.db_change(deactivate_existing_user, [username])

            data = json.dumps({'result': 'OK'})
            return data
        else:
            error_result = json.dumps({'result': 'Error: User Not Found'})
            return error_result
