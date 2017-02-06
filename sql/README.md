<h1>The Data and Database Creation</h1>

<p><i>This directory is provided by Daniel Ellsworth, the teacher for CIS322</i></p>

<h4>CONTENTS</h4>
<ul>
<li><b>create_tables.sql</b> - SQL script which creates empty tables for LOST postgreSQL database</li>
<li><b>import_data.sh</b> - Bash script that creates empty tables, downloads legacy data, unzips it, runs supporting python files, and cleans up after itself</li>
<li><b>do_transit.py</b> - Processes the transit data</li>
<li><b>facilities_map.sql</b> - Loads the static data on the facilities</li>
<li><b>norm_tags.py</b> - Rewrites some of the data so that it is easier to process</li>
<li><b>prep_inv.py</b> - Converts *_inventory.csv to sql</li>
<li><b>prep_prod.py</b> - Converts product info to sql</li>
<li><b>prep_sec.py</b> - Converts security info to sql</li>
<li><b>prepend_fcode</b> - Concatenates the inventory data and annotates with source facility
<li><b>waypoints.py</b> - Processes the convoy file</li>
<li><b>backfill.sql</b> - A script to fill in a few inferences</li>
</ul>

<br>

<h4>USAGE</h4>
<ol>
<li><code>$ createdb lost</code></li>
<li><code>$ ./import_data.sh</code></li>
</ol>

<br>

<h4>INFO FROM THE TEACHER</h4>
<p>To test the LOST database after the OSNAP data has been migrated, the following queries have been suggests. These queries are untested but should have the right basic structure. If you compare the queries to the entity relationship diagram you should be able to trace the path between the assets and facilities.</p>

<small>This query successfully returning all assets at least once is enough to get credit</small>
<br>
<code>
SELECT fcode,asset_tag
FROM assets a
LEFT JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
LEFT JOIN facilities f ON aa.facility_fk=f.facility_pk
</code>

<small>This query is more complex... only the facility an asset is currently at. Assets in transit will be missed</small>
<br>
<code>
SELECT fcode,asset_tag 
FROM assets a
JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE aa.arrive_dt < now() and (aa.depart_dt is NULL or aa.depart_dt > now())
</code>

<small>This query should pick up the assets currently in transit</small>
<br>
<code>
SELECT request_id,asset_tag 
FROM assets a
JOIN asset_on aa  ON a.asset_pk=aa.asset_fk
JOIN convoys c ON aa.convoy_fk=c.convoy_pk
WHERE aa.load_dt < now() and (aa.unload_dt is NULL or aa.unload_dt > now())
</code>