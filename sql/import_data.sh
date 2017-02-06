#! /bin/bash
db_name=$1
port=$2


#############################
# CREATE DB & GET CSV FILES #
#############################
printf '\e[1;34mCreating empty tables for database model...\n\e[0m'
psql lost < create_tables.sql

printf '\e[1;34mCurling in OSNAP legacy data...\n\e[0m'
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz

printf '\e[1;34mUnzipping compressed data...\n\e[0m'
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv


#############################
# CONVERT CSV TO POSTGRESQL #
#############################
printf '\e[1;34mAttempting to populate database from legacy data...\n\e[0m'
python3 csv2psql.py $db_name $port


##################################################
# Piping in and cleaning up generated .sql files #
##################################################
# Security Data
psql $1 -f sec_load.sql
rm sec_load.sql

# Product Data
psql $1 -f prod_load.sql
rm prod_load.sql

#



printf '\e[1;34mGarbage collection taking place...\n\e[0m'
rm -rf osnap_legacy
rm osnap_legacy.tar.gz

printf '\e[1;34m~~~COMPLETE~~~\n\n\e[0m'