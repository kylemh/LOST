from flask import request, render_template, flash

from app import app, helpers


@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    if request.method == 'POST':
        fcode = request.form.get('fcode', None).strip()
        common_name = request.form.get('common_name', None)
        location = request.form.get('location', None)

        # Get all current facilities for table population
        all_facilities = helpers.db_query("SELECT * FROM facilities;", [])

        # If something is missing from the form...
        if not fcode or not common_name or not location:
            flash('Please complete the form')
            return render_template('add_facility.html', data=all_facilities)

        else:
            # Check for duplicate entry attempt...
            matching_facilities = ("SELECT facility_pk FROM facilities "
                                   "WHERE fcode=%s OR common_name=%s;")
            facility_does_exist = helpers.duplicate_check(matching_facilities, [fcode, common_name])

            if facility_does_exist:
                flash('There already exists a facility with that fcode or common name!')
                return render_template('add_facility.html', data=all_facilities)

            # Facility does not already exist - create it
            else:
                new_facility = ("INSERT INTO facilities (fcode, common_name, location) "
                                "VALUES (%s, %s, %s);")
                helpers.db_change(new_facility, [fcode, common_name, location])
                flash('New facility was created!')

    # Update all_facilities after insert, but before template rendering
    all_facilities = helpers.db_query("SELECT * FROM facilities;", [])

    # Database doesn't have any facilities yet.
    if all_facilities is None:
        all_facilities = [('NO FACILITIES', 'NO FACILITIES', 'NO FACILITIES')]

    return render_template('add_facility.html', data=all_facilities)
