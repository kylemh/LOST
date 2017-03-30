#! /bin/bash

# preflight.sh
# This script handles the setup that must occur prior to running lost.py


if [ "$#" -ne 1 ]; then
    printf '\e[1;34m\nERROR NO DBNAME - Usage: ./preflight.sh <dbname>\n\e[0m'
    exit;
fi

printf '\e[1;34m\n~~~CREATING USERS TABLE~~~\n\e[0m'
cd sql
psql $1 -f create_tables.sql
cd ..
