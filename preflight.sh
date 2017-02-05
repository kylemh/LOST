#! /bin/bash

# preflight.sh

# NOTE: This script handles preconfiguration of my Flask application

printf 'Moving into place...\n'
cd sql

printf 'Importing data from legacy documents...\n'
/sql/import_data.sh

printf 'Moving to application environment...\n'
cd ..

printf 'Installing wsgi files...'
cp -R src/* $HOME/wsgi
printf 'COMPLETE!\n\n'