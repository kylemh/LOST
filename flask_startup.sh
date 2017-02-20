#!/bin/bash

# set local variables
URL=$1
DB_NAME=hw
PORT=5432

# set the path
# (I pass this script to the VM from another script running on my host
# machine ... this isn't necessary if calling this script directly on the VM)
# PATH=/osnap/bin:$PATH

# note: for the next commands, we assume that the postgres server is already
#       running (pg_ctl ...)

# note: since we are creating a testing db here, with a specified name, your
#       preflight.sh shouldn't create a database and your application shouldn't
#       depend on a hardcoded database name

# remove the db if it exists already
dropdb -p $PORT $DB_NAME

# create db
createdb -p $PORT $DB_NAME

# pull student repo
git clone $URL CIS322
cd CIS322

# run preflight
. preflight.sh $DB_NAME

# get config file from ix (database name is 'hw')
cd src
curl -O http://ix.cs.uoregon.edu/~hampton2/322/lost_config.json

# also copy config to wsgi folder
cp lost_config.json ~/wsgi/
