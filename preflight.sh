#! /bin/bash

# preflight.sh
# This script handles the setup that must occur prior to running app.py


if [ "$#" -ne 1 ]; then
    printf '\e[1;34m\nERROR NO DBNAME - Usage: ./preflight.sh <dbname>\n\e[0m'
    exit;
fi

printf '\e[1;34m\n~~~CREATING USERS TABLE~~~\n\e[0m'
cd sql
psql $1 -f create_tables.sql
cd ..

printf '\e[1;34m~~~COPYING RELEVANT WSGI FILES~~~\n\e[0m'
cp -R src/* $HOME/wsgi

printf '\e[1;34m~~~RESTARTING APACHE~~~\n\e[0m'
apachectl restart