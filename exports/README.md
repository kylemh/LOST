<h2>Data Export</h2>
<p>This directory contains scripts and files necessary to export a representational look at LOST's current data via .csv files.<p>

<br>

<h4>Usage</h4>
`$ export_data.sh $database_name> $output_directory`

<br>

<h4>File Structure</h4>
```
.
├── assets.csv
├── export_data.sh
├── facilities.csv
├── migrations.py
├── transfers.csv
└── users.csv
```
export_data.sh - a bash script to automate migration process

migrations.py - python module to convert database tables to csv files

users.csv - a csv file containing user information

facilities.csv - a csv file containing LOST facility information

assets.csv - a csv file containing LOST assets

transfers.csv - a csv file containing transfer information

<br>

<h4>File Details</h4>
<h6>users.csv</h6>
<b>The users.csv file contains user information needed to reconstruct user accounts and is in CSV format.</b>

The CSV file will contain the following columns in order:
<br>
<ul>
    <li>username - login username
    <li>password - login password
    <li>role - user role (Logistics Officer or Facilities Officer)
    <li>active - True if the user is currently allowed to login, otherwise False
</ul>

<h6>facilities.csv</h6>
<b>The facilities.csv file contain the list of facilities and is in CSV format.</b> 

The CSV file will contain the following columns in order:
<br>
<ul>
    <li>fcode - The facility code for the facility
    <li>common_name - A more human friendly name for the facility
</ul>

<h6>assets.csv</h6>
<b>The assets.csv file lists the individual assets and is in CSV format.</b>

The CSV file will contain the following columns in order:

<ul>
    <li>asset_tag - The unique LOST asset tag for the asset
    <li>description - A description of the asset
    <li>facility - The initial facility the asset was located at
    <li>acquired - The date the asset was acquired in ISO date format
    <li>disposed - The date the asset was disposed in ISO date format or the string NULL
</ul>

<h6>transfers.csv</h6>
<b>The transfers.csv file contains the history of motion for assets and is in CSV format.</b>

The CSV file will contain the following columns in order:

<ul>
    <li>asset_tag - The unique LOST asset tage for the asset
    <li>request_by - The username of the user requesting the transfer
    <li>request_dt - The date the request was submitted in ISO date format
    <li>approve_by - The username of the user approving or rejecting the transfer
    <li>approve_dt - The date the request was approved in ISO date format
    <li>source - The fcode of the facility the asset started at
    <li>destination - The fcode of the facility the asset moved to
    <li>load_dt - The date the asset was loaded at the source in ISO date format
    vunload_dt - The date the asset was unloaded at the destination in ISO date format
</ul>
