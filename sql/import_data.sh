#! /bin/bash
db_name=$1
port=$2

printf '\e[1;34mCreating empty tables for database model...\n\e[0m'
psql lost < create_tables.sql

printf '\e[1;34mCurling in OSNAP legacy data...\n\e[0m'
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz

printf '\e[1;34mUnzipping compressed data...\n\e[0m'
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv

printf '\e[1;34mAttempting to populate database from legacy data...\n\e[0m'
python3 csv2psql.py $db_name $port

printf '\e[1;34mGarbage collection taking place...\n\e[0m'
rm -rf osnap_legacy
rm osnap_legacy.tar.gz

printf '\e[1;34m~~~COMPLETE~~~\n\n\e[0m'