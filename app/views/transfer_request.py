from flask import session, request, flash, render_template, redirect, url_for
import datetime

from app import app, helpers


@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    # Not a logistics officer...
    if session.get('perms') != 2:
        flash('You are not a Logistics Officer. You do not have permissions to request transfers!')
        return render_template('dashboard.html')

    request_is_post = False
    if request.method == 'POST':
        request_is_post = True
        asset_key = request.form['asset']
        src_facility = request.form['src_facility']
        dest_facility = request.form['dest_facility']

        # Form Completion Validation
        if asset_key == '':
            flash('Please select an asset.')
            return redirect(url_for('transfer_req'))
        elif src_facility == '' or dest_facility == '':
            flash('Please select a facility.')
            return redirect(url_for('transfer_req'))

        location_query = ("SELECT asset_at.facility_fk FROM asset_at "
                          "JOIN assets ON asset_at.asset_fk = assets.asset_pk "
                          "WHERE asset_pk = %s;")
        actual_asset_location = helpers.db_query(location_query, [asset_key])

        if actual_asset_location is None:
            flash('There is either no facilities or assets in the database.')
            return redirect(url_for('dashboard'))

        if src_facility != str(actual_asset_location[0][0]):
            flash('The source facility you selected is not where the asset is stored.')
            return redirect(url_for('transfer_req'))
        elif dest_facility == src_facility:
            flash('Please select different facilities in order to submit a transfer request.')
            return redirect(url_for('transfer_req'))

        # Inputs Validated
        else:
            request_sql = ("INSERT INTO requests "
                           "(asset_fk, user_fk, src_fk, dest_fk, request_dt, approved, completed) "
                           "VALUES "
                           "(%s, %s, %s, %s, %s, 'False', 'False');")

            helpers.db_change(
                request_sql, [
                    asset_key,
                    session['user_id'],
                    src_facility,
                    dest_facility,
                    datetime.datetime.now()
                ]
            )

            flash('Request Submitted. Please await Facility Officer approval.')

    # Query relevant data for dropdown selections
    # Facilities
    all_facilities_query = "SELECT * FROM facilities;"
    all_facilities = helpers.db_query(all_facilities_query, [])

    if all_facilities is None:
        flash('You must add facilities to the database before you can create transfer requests.')
        return redirect(url_for('dashboard'))

    # Assets
    all_assets_query = ("SELECT * FROM assets WHERE asset_pk NOT IN "
                        "(SELECT asset_fk FROM requests "
                        "WHERE completed='FALSE' AND approved='FALSE')"
                        ";")
    all_assets = helpers.db_query(all_assets_query, [])

    # Handle empty result query cases
    if request_is_post and all_assets is None:
        flash('You must add assets to the database before you can create transfer requests.')
        return redirect(url_for('dashboard'))

    return render_template('transfer_req.html', asset_list=all_assets, facility_list=all_facilities)
