#! /bin/bash

# This script is for migrating OSNAP legacy data into the LOST database. Write your own
# scripts for the data migration. If we find wholesale copying of functional portions of 
# this code in your final project deliverable, 0 points will be awarded for the data
# migration.

# Some of these scripts handle cases not present in the sample dataset but seem likely to
# actually occur... The additional logic was written defensively and out of habit.

# to speed up dev, put the db in a fresh state
#dropdb $1
#createdb $1
#psql $1 -f create_tables.sql

# Load the security data
python3 prep_sec.py
psql $1 -f sec_load.sql
rm sec_load.sql

# Load the facilities -- A list is not provided in the data but may be inferred from the 
# provided data... This list should be asked for from the customer
psql $1 -f facilities_map.sql

# Handle the product data, such as it is
python3 prep_prod.py
psql $1 -f prod_load.sql
rm prod_load.sql

# Handle the facility inventories
python3 prepend_fcode.py osnap_legacy/*_inventory.csv > all_inventory.csv
python3 prep_inv.py all_inventory.csv
rm all_inventory.csv
psql $1 -f inv_load.sql
rm inv_load.sql

# Handle make convoys from the transit data... seems easier than from the convoy data
python3 norm_tags.py > transit.csv
# This next step gets tricky, the assets may or may not exist in the data...
# Would be easier if Postgres supported UPSERT by default.
python3 do_transit.py $1 $2
rm transit.csv

# Handle the convoy data, add waypoints and missing assets
python3 waypoints.py $1 $2

# Need to backfill some asset records that can be inferred from the imported data
psql $1 -f backfill.sql
