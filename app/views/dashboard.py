from flask import session, request, url_for, redirect, flash, render_template
import datetime

from app import app, helpers


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        flash('You must login before being allowed access to the dashboard')
        return redirect(url_for('login'))

    cur_user = session['username']

    # POST METHOD
    if request.method == 'POST':
        # LOGISTICS OFFICER
        if session['perms'] == 2:
            selected_request = request.form.get('request_pk', None)
            load_date = request.form.get('load date', None)
            unload_date = request.form.get('unload date', None)

            # Form Completion Check
            if not selected_request:
                flash('Please choose a request to edit.')
                return redirect(url_for('dashboard'))
            elif selected_request == 'NO REQUESTS':
                flash('There are no requests to edit.')
                return redirect(url_for('dashboard'))
            elif not load_date and not unload_date:
                flash('Please at least fill in a load date.')
                return redirect(url_for('dashboard'))

            selected_request_query = ("SELECT "
                                      "r.request_pk, r.asset_fk, r.src_fk, r.dest_fk, aa.arrive_dt "
                                      "FROM requests as r "
                                      "JOIN asset_at as aa ON r.asset_fk = aa.asset_fk "
                                      "WHERE request_pk = %s;")
            selected_request_record = helpers.db_query(selected_request_query, [selected_request])

            # Both load and unload date submitted
            if load_date and unload_date:
                # Impossible use case
                if load_date > unload_date:
                    flash(
                        'It is not possible for an asset to be loaded after '
                        'it was unloaded. Make sure you entered your '
                        'dates correctly.'
                    )
                else:
                    # Check for logical dates...
                    transit_update = ("UPDATE in_transit SET load_dt = %s, unload_dt = %s "
                                      "WHERE request_fk = %s;")
                    helpers.db_change(transit_update, [
                        load_date, unload_date, selected_request]
                    )

                    update_asset_at = ("UPDATE asset_at SET depart_dt = %s "
                                       "WHERE asset_fk = %s AND arrive_dt = %s;")
                    helpers.db_change(update_asset_at, [
                        load_date, selected_request_record[0][1], selected_request_record[0][4]]
                    )

                    new_asset_at = ("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) "
                                    "VALUES (%s, %s, %s);")
                    helpers.db_change(new_asset_at, [
                        selected_request_record[0][1], selected_request_record[0][3], unload_date]
                    )

                    update_request = "UPDATE requests SET completed = TRUE WHERE request_pk = %s;"
                    helpers.db_change(update_request, [
                        selected_request]
                    )

                    flash('Transfer Completed - Request Completed')

            # Updating only load date
            elif load_date and not unload_date:
                transit_update = "UPDATE in_transit SET load_dt = %s WHERE request_fk = %s;"
                helpers.db_change(transit_update, [
                        load_date, selected_request]
                )

                update_asset_at = ("UPDATE asset_at SET depart_dt = %s "
                                   "WHERE asset_fk = %s AND arrive_dt = %s;")
                helpers.db_change(update_asset_at, [
                        load_date, selected_request_record[0][1], selected_request_record[0][4]]
                )

                flash('Load Date Updated')

            # Attempting to only update unload date
            else:
                load_date = """
                SELECT r.request_pk, t.load_dt FROM requests as r
                JOIN in_transit as t ON r.request_pk = t.request_fk
                WHERE r.approved = TRUE AND r.request_pk = %s;
                """
                lo_requests = helpers.db_query(load_date, [selected_request])

                # There is no load date for this asset
                if not lo_requests[0][1]:
                    flash('The asset must be loaded before it can be unloaded.')

                # There is a load date for this asset-in-transit
                else:
                    transit_update = "UPDATE in_transit SET unload_dt = %s WHERE request_fk = %s;"
                    helpers.db_change(transit_update, [
                            unload_date, selected_request]
                    )

                    new_asset_at = ("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) "
                                    "VALUES (%s, %s, %s);")
                    helpers.db_change(new_asset_at, [
                            selected_request_record[0][1],
                            selected_request_record[0][3],
                            unload_date
                        ]
                    )

                    update_request = "UPDATE requests SET completed = TRUE WHERE request_pk = %s;"
                    helpers.db_change(update_request, [
                            selected_request]
                    )

                    flash('Unload Date Updated! Transfer Completed - Request Completed')

            # Populate Table
            requests_query = ("SELECT r.request_pk, a.asset_tag, r.user_fk, "
                              "f1.common_name, f2.common_name, t.load_dt, t.unload_dt "
                              "FROM requests as r JOIN assets as a ON r.asset_fk = a.asset_pk "
                              "JOIN facilities as f1 on r.src_fk = f1.facility_pk "
                              "JOIN facilities as f2 on r.dest_fk = f2.facility_pk "
                              "JOIN in_transit as t ON r.request_pk = t.request_fk "
                              "WHERE r.approved = TRUE AND r.completed = FALSE;")
            lo_requests = helpers.db_query(requests_query, [])

            if lo_requests is None:
                lo_requests = [
                    ('NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS',
                     'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS')
                ]

            return render_template('dashboard.html', user=cur_user, requests=lo_requests)

        # FACILITY OFFICER
        elif session['perms'] == 3:
            selected_request = request.form.get('request_pk', None)

            # Nothing Selected
            if not selected_request:
                flash('Please select a request.')

            # No requests in DB
            elif selected_request == 'NO REQUESTS':
                flash('There are no requests to approve/disapprove.')

            # Something selected
            else:
                # Request rejected (Marked as completed)
                if 'reject' in request.form:
                    reject_request = "UPDATE requests SET completed = TRUE WHERE request_pk = %s;"
                    helpers.db_change(reject_request, [selected_request])
                    flash('Request DENIED.')

                # Request Approved
                else:
                    update_request_sql = ("UPDATE requests SET "
                                          "approved = TRUE, "
                                          "approving_user_fk = %s, "
                                          "approve_dt = %s "
                                          "WHERE request_pk = %s;")
                    helpers.db_change(update_request_sql, [
                            session['user_id'], datetime.datetime.now(), selected_request]
                    )

                    transit_sql = "INSERT INTO in_transit (request_fk) VALUES (%s);"
                    helpers.db_change(transit_sql, [selected_request])

                    flash('Request APPROVED.')

            # Populate Table
            requests_query = ("SELECT r.request_pk, a.asset_tag, r.user_fk, "
                              "f1.common_name, f2.common_name FROM requests as r "
                              "JOIN assets as a ON r.asset_fk = a.asset_pk "
                              "JOIN facilities as f1 ON r.src_fk = f1.facility_pk "
                              "JOIN facilities as f2 ON r.dest_fk = f2.facility_pk "
                              "WHERE r.approved = FALSE AND r.completed = FALSE;")
            fo_requests = helpers.db_query(requests_query, [])

            if fo_requests is None:
                fo_requests = [
                    ('NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS')
                ]

            return render_template('dashboard.html', user=cur_user, requests=fo_requests)

    # GET METHOD
    else:
        # LOGISTICS OFFICER
        if session['perms'] == 2:
            requests_query = ("SELECT r.request_pk, a.asset_tag, r.user_fk, "
                              "f1.common_name, f2.common_name, t.load_dt, t.unload_dt "
                              "FROM requests as r JOIN assets as a ON r.asset_fk = a.asset_pk "
                              "JOIN facilities as f1 on r.src_fk = f1.facility_pk "
                              "JOIN facilities as f2 on r.dest_fk = f2.facility_pk "
                              "JOIN in_transit as t ON r.request_pk = t.request_fk "
                              "WHERE r.approved = TRUE AND r.completed = FALSE;")
            lo_requests = helpers.db_query(requests_query, [])

            if lo_requests is None:
                lo_requests = [
                    ('NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS',
                     'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS')
                ]

            return render_template('dashboard.html', user=cur_user, requests=lo_requests)

        # FACILITY OFFICER
        elif session['perms'] == 3:
            requests_query = ("SELECT r.request_pk, a.asset_tag, r.user_fk, "
                              "f1.common_name, f2.common_name FROM requests as r "
                              "JOIN assets as a ON r.asset_fk = a.asset_pk "
                              "JOIN facilities as f1 ON r.src_fk = f1.facility_pk "
                              "JOIN facilities as f2 ON r.dest_fk = f2.facility_pk "
                              "WHERE r.approved = FALSE AND r.completed = FALSE;")
            fo_requests = helpers.db_query(requests_query, [])

            if fo_requests is None:
                fo_requests = [
                    ('NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS', 'NO REQUESTS')
                ]

            return render_template('dashboard.html', user=cur_user,
                                   requests=fo_requests)

        else:
            flash('You do not have access. Please login or create an account.')
            redirect(url_for('login'))


@app.route('/approve_req', methods=['GET'])
def approve_req():
    if session['perms'] == 3:
        pass
    else:
        flash('You must be a facility officer to approve requests.')
    return redirect(url_for('dashboard'))


@app.route('/update_transit', methods=['GET'])
def update_transit():
    if session['perms'] == 2:
        pass
    else:
        flash('You must be a logistics officer to update transit records.')
    return redirect(url_for('dashboard'))
