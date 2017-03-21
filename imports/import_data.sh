#! /bin/bash

# Check for correct number of commandline arguments
if [ "$#" -ne 2 ]; then
	echo "\e[1;34mUsage: ./import_data.sh <dbname> <input dir>\e[0m"
	exit;
fi

database_name=$1
input_directory=$2

python3 import.py database_name input_directory

echo "\e[1;34m\nData Import Complete\n\e[0m"
