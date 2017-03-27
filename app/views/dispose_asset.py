from flask import session, flash, render_template, request

from app import app, helpers


# TODO: Implement functionality for asset being set to disposed if moved from original facility
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    # Not a logistics officer...
    if session.get('perms') != 2:
        flash('You are not a Logistics Officer. You do not have permissions to remove assets!')
        return render_template('dashboard.html')

    # Get all current assets for table population
    else:
        all_assets_query = ("SELECT assets.asset_tag, assets.description, "
                            "facilities.location, assets.disposed "
                            "FROM assets JOIN asset_at ON assets.asset_pk = asset_at.asset_fk "
                            "JOIN facilities ON asset_at.facility_fk = facilities.facility_pk;")
        all_assets = helpers.db_query(all_assets_query, [])

        # Handle table when no assets in database
        if all_assets is None:
            all_assets = [(
                'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES'
            )]
            flash('There are currently no assets to remove')
            return render_template('dispose_asset.html', assets_list=all_assets)

        if request.method == 'POST':
            asset_tag = request.form.get('asset_tag', None).strip()
            date = request.form.get('date')

            # If something is missing from the form...
            if not asset_tag or not date:
                flash('Please complete the form')
                return render_template('dispose_asset.html', assets_list=all_assets)
            else:
                try:
                    validated_date = helpers.validate_date(date)
                except ValueError or TypeError or UnboundLocalError:
                    flash('Please enter the date in the following format: MM/DD/YYYY')
                    return render_template('dispose_asset.html', assets_list=all_assets)

                # Check for matching tag...
                matching_asset = "SELECT asset_pk FROM assets WHERE asset_tag = %s;"
                asset_does_exist = helpers.duplicate_check(matching_asset, [asset_tag])

                if asset_does_exist:
                    # Get asset_fk for asset_at update (returns a tuple in an array)
                    asset_fk = helpers.db_query(matching_asset, [asset_tag])[0][0]

                    # Change asset_at table to reflect impending disposal
                    update_asset_at = "UPDATE asset_at SET depart_dt=%s WHERE asset_fk=%s;"
                    helpers.db_change(update_asset_at, [validated_date, asset_fk])

                    # Remove asset from assets
                    asset_to_dispose = "UPDATE assets SET disposed=TRUE WHERE asset_tag = %s;"
                    helpers.db_change(asset_to_dispose, [asset_tag])

                    # Update current assets for view's table ('disposed' column will have changed)
                    all_assets = helpers.db_query(all_assets_query, [])

                    # Handle table when no assets in database
                    if all_assets is None:
                        all_assets = [(
                            'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES', 'NO ENTRIES'
                        )]

                    flash('Asset removed!')
                    return render_template('dispose_asset.html', assets_list=all_assets)

                else:
                    flash('There does not exist an asset with that tag!')
                    return render_template('dispose_asset.html', assets_list=all_assets)

        return render_template('dispose_asset.html', assets_list=all_assets)
