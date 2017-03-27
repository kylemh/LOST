from flask import request, flash, redirect, url_for, render_template

from app import app, helpers


@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    all_facilities_query = "SELECT * FROM facilities;"

    # If a form has been submitted...
    if request.method == 'POST':
        # List of single-tuples of all facilities to populate drop-down
        all_facilities = helpers.db_query(all_facilities_query, [])
        if all_facilities is None:
            flash('You must add facilities before you can get asset reports.')
            return redirect(url_for('dashboard'))

        # User Input from Form
        facility = request.form.get('facility')
        date = request.form.get('date')

        # Validate Inputs
        if not date:
            flash('Please complete the form')
            return render_template(
                'asset_report.html', facilities_list=all_facilities, report=False
            )
        else:
            try:
                validated_date = helpers.validate_date(date)
            except ValueError or TypeError or UnboundLocalError:
                flash(
                    'Please enter the date in the following format: MM/DD/YYYY')
                return render_template(
                    'asset_report.html', facilities_list=all_facilities, report=False
                )

        # Get all assets at all facilities
        if facility == 'All':
            all_assets_report = ("SELECT a.asset_tag, a.description, f.location, "
                                 "a_a.arrive_dt, a_a.depart_dt FROM assets as a "
                                 "JOIN asset_at as a_a ON a.asset_pk = a_a.asset_fk "
                                 "JOIN facilities as f ON a_a.facility_fk = f.facility_pk "
                                 "WHERE (a_a.depart_dt >= %s OR a_a.depart_dt IS NULL) "
                                 "AND a_a.arrive_dt <= %s;")
            all_assets = helpers.db_query(
                all_assets_report, [validated_date, validated_date]
            )

            # No Results
            if all_assets is None:
                all_assets = [(
                    'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES'
                )]

            # Handle <h4> at top of asset_report for all facilities option - searched by facility[2]
            facility = ['', '', 'all facilities']

            return render_template(
                'asset_report.html', facility=facility, date=validated_date,
                assets_list=all_assets, facilities_list=all_facilities, report=True
            )

        # Get all assets at a specific facility
        else:
            individual_facility_report = ("SELECT a.asset_tag, a.description, "
                                          "f.location, a_a.arrive_dt, a_a.depart_dt "
                                          "FROM assets as a "
                                          "JOIN asset_at as a_a ON a.asset_pk = a_a.asset_fk "
                                          "JOIN ("
                                          "SELECT facility_pk, location FROM facilities "
                                          "WHERE facility_pk = %s"
                                          ") as f ON f.facility_pk = a_a.facility_fk "
                                          "WHERE (a_a.depart_dt >= %s OR a_a.depart_dt IS NULL) "
                                          "AND a_a.arrive_dt <= %s;")
            filtered_assets = helpers.db_query(
                individual_facility_report, [facility, validated_date, validated_date]
            )

            # No Results
            if filtered_assets is None:
                filtered_assets = [(
                    'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES'
                )]

            # Handle <h4> at top of asset_report for all facilities option - searched by facility[2]
            facility = filtered_assets[0]

            return render_template('asset_report.html', facility=facility, date=validated_date,
                                   assets_list=filtered_assets, facilities_list=all_facilities,
                                   report=True)

    # List of single-tuples of all facilities to populate drop-down
    all_facilities = helpers.db_query(all_facilities_query, [])
    if all_facilities is None:
        flash('You must add facilities to the database before you can get asset reports.')
        return redirect(url_for('dashboard'))

    return render_template('asset_report.html', facilities_list=all_facilities, report=False)
