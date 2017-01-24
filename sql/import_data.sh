#! /bin/bash
db_name = $1
port = $2

echo 'Creating database...'
createdb lost

echo 'Creating empty tables for database model...'
psql create_tables.sql

echo 'Curling in OSNAP legacy data...'
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz

echo 'Unzipping compressed data...'
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv

echo 'Attempting to populate database from legacy data...'
python3 csv2psql.py $db_name $port

echo 'Garbage collection taking place...'
rm -rf osnap_legacy
rm osnap_legacy.tar.gz

echo '~~~COMPLETE~~~'
