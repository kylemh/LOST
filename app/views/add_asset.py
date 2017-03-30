from flask import request, flash, url_for, redirect, render_template

from app import app, helpers


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    # Create queries to populate dropdown menu and current assets table
    all_assets_query = ("SELECT assets.asset_tag, assets.description, facilities.location "
                        "FROM assets "
                        "JOIN asset_at ON assets.asset_pk = asset_at.asset_fk "
                        "JOIN facilities ON asset_at.facility_fk = facilities.facility_pk;")
    all_facilities_query = "SELECT * FROM facilities;"

    if request.method == 'POST':
        asset_tag = request.form.get('asset_tag', None).strip()
        description = request.form.get('description', None)
        facility = request.form.get('facility')
        date = request.form.get('date')
        disposed = False

        # Get all current assets and facilities for table/drop-down population
        all_assets = helpers.db_query(all_assets_query, [])
        all_facilities = helpers.db_query(all_facilities_query, [])

        if all_facilities is None:
            flash('You must add facilities before you can get asset reports.')
            return redirect(url_for('dashboard'))

        # Handle table when no assets in database
        if all_assets is None:
            all_assets = [
                ('NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES')
            ]

        # If something is missing from the form...
        if not asset_tag or not description or not date or facility == '':
            flash('Please complete the form')
            return render_template(
                'add_asset.html', assets_list=all_assets, facilities_list=all_facilities
            )
        else:
            try:
                validated_date = helpers.validate_date(date)
            except ValueError or TypeError or UnboundLocalError:
                flash('Please enter the date in the following format: MM/DD/YYYY')
                return render_template(
                    'add_asset.html', assets_list=all_assets, facilities_list=all_facilities
                )

            # Check for duplicate entry attempt...
            matching_assets = "SELECT asset_pk FROM assets WHERE asset_tag=%s;"
            asset_does_exist = helpers.duplicate_check(matching_assets, [asset_tag])

            if asset_does_exist:
                flash('There already exists an asset with that tag!')
            else:
                # Asset does not already exist - create it...
                new_asset = ("INSERT INTO assets (asset_tag, description, disposed) "
                             "VALUES (%s, %s, %s);")
                helpers.db_change(new_asset, [asset_tag, description, disposed])

                # Get Asset Key for asset_at insertion
                recently_added_asset = "SELECT asset_pk FROM assets WHERE asset_tag = %s;"
                asset_fk = helpers.db_query(recently_added_asset, [asset_tag])

                # Insert asset_at record for newly added asset
                new_asset_at = ("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) "
                                "VALUES (%s, %s, %s);")
                helpers.db_change(new_asset_at, [asset_fk[0][0], facility, validated_date])

                flash('New asset added!')

    # Get Facilities for dropdown
    all_facilities = helpers.db_query(all_facilities_query, [])
    if all_facilities is None:
        flash('You must add facilities before you can get asset reports.')
        return redirect(url_for('dashboard'))

    # Update all_assets after insert, but before template rendering
    all_assets = helpers.db_query(all_assets_query, [])

    # Handle situation of no assets in database
    if all_assets is None:
        all_assets = [('NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES')]

    return render_template('add_asset.html', assets_list=all_assets, facilities_list=all_facilities)

