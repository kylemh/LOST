#! /bin/bash
db_name=$1
port=$2

#############################
# CREATE DB & GET CSV FILES #
#############################
printf '\e[1;34m\nCreating empty tables for database model...\n\e[0m'
psql $1 < create_tables.sql

printf '\e[1;34m\nCurling in OSNAP legacy data...\n\e[0m'
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz

printf '\e[1;34m\nUnzipping compressed data...\n\e[0m'
tar -xvf osnap_legacy.tar.gz


#############################
# POPULATE DATABASE #
#############################
printf '\e[1;34m\nFilling tables...\n\e[0m'
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
