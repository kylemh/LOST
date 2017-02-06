#! /bin/bash
db_name=$1
port=5432

printf 'Creating empty tables for database model...\n'
psql lost < create_tables.sql

printf 'Curling in OSNAP legacy data...\n'
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz

printf 'Unzipping compressed data...\n'
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv

printf 'Attempting to populate database from legacy data...\n'
python3 csv2psql.py $db_name $port

printf 'Garbage collection taking place...\n'
rm -rf osnap_legacy
rm osnap_legacy.tar.gz

printf '~~~COMPLETE~~~\n\n'