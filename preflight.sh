#! /bin/bash

# preflight.sh

# This script handles the setup that must occur prior to running LOST
# Specifically this script:
#    1. creates the database
#    2. imports the legacy data
#    3. copies the required source to $HOME/wsgi

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

printf 'Moving into database directory...\n'
cd sql

printf 'Importing data from legacy documents...\n'
bash ./import_data.sh $1 5432

printf 'Moving to application environment...\n'
cd ..

printf 'Installing wsgi files...'
cp -R src/* $HOME/wsgi
printf 'COMPLETE!\n\n'