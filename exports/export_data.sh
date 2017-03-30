#! /bin/bash

# Check for correct number of commandline arguments
if [ "$#" -ne 2 ]; then
	echo "\e[1;34mUsage: ./export_data.sh <dbname> <output dir>\e[0m"
	exit;
fi

python3 migration.py $1
mkdir --parents $2
mv *.csv $2

echo "\e[1;34m\nData Export Complete\n\e[0m"