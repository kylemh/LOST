#! /bin/bash

# preflight.sh

# This script handles the setup that must occur prior to running LOST
# Specifically this script:
#    1. creates the database
#    2. imports the legacy data
#    3. copies the required source to $HOME/wsgi

if [ "$#" -ne 1 ]; then
    printf '\e[1;34mUsage: ./preflight.sh <dbname>\n\e[0m'
    exit;
fi

printf '\e[1;34mMoving into database directory...\n\e[0m'
cd sql

printf '\e[1;34mImporting data from legacy documents...\n\e[0m'
bash ./import_data.sh $1 5432

printf '\e[1;34mMoving to application environment...\n\e[0m'
cd ..

printf '\e[1;34mInstalling wsgi files...\e[0m'
cp -R src/* $HOME/wsgi
printf '\e[1;34m~~~COMPLETE~~~\n\n\e[0m'
