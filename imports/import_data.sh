#! /bin/bash

# Check for correct number of commandline arguments
if [ "$#" -ne 2 ]; then
	echo "\e[1;34mUsage: ./import_data.sh <dbname> <input dir>\e[0m"
	exit;
fi

python3 import.py $1 $2

echo "\e[1;34m\nData Import Complete\n\e[0m"
