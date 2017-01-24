<h1>The Data and the Database</h1>

<h4>CONTENTS</h4>
<ul>
<li><b>create_tables.sql</b> - SQL script which creates empty tables for LOST postgreSQL database</li>
<li><b>csv2psql.py</b> - Python script that converts legacy data (.csv) into entries within the LOST database</li>
<li><b>import_data.sh</b> - Bash script that you should run after <code>$ createdb lost</code> creates empty tables, downloads legacy data, unzips it, runs csv2psql.py, and cleans up after itself</li>
</ul>

<h4>USAGE</h4>
<p>$ ./import_data.sh</p>

<i>TODO: Add bash scripts and documentation to allow for deployment on ANY linux-apache server</i>
