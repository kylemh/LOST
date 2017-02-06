import csv
import sys
import re
import datetime
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def parse_time(ts):
    m = re.match(r'(\d+)/(\d+)/(\d+)\s+(\d+):(\d+)',ts)
    mon = int(m.group(1))
    day = int(m.group(2))
    yr  = int(m.group(3))+2000
    hr  = int(m.group(4))
    min = int(m.group(5))
    return datetime.datetime(yr,mon,day,hr,min)
    
def vehicle_upsert(asset_tag):
    cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
    r = cur.fetchone()
    if not r:
        cur.execute("INSERT INTO assets (asset_tag) VALUES (%s)",(asset_tag,))
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
        asset_pk = cur.fetchone()[0]
    else:
        asset_pk = r[0]
    cur.execute("SELECT vehicle_pk FROM vehicles WHERE asset_fk=%s",(asset_pk,))
    r = cur.fetchone()
    if not r:
        cur.execute("INSERT INTO vehicles (asset_fk) VALUES (%s)",(asset_pk,))
        cur.execute("SELECT vehicle_pk FROM vehicles WHERE asset_fk=%s",(asset_pk,))
        r = cur.fetchone()
    return r[0]

def used_upsert(v_pk, c_pk):
    cur.execute("SELECT count(*) FROM used_by WHERE vehicle_fk=%s and convoy_fk=%s",(v_pk,c_pk))
    if cur.fetchone()[0] > 0:
        return
    cur.execute("INSERT INTO used_by (vehicle_fk,convoy_fk) VALUES (%s,%s)",(v_pk,c_pk))
    
def process_waypoints():
    with open('osnap_legacy/convoy.csv') as f:
        data = csv.DictReader(f)
        for r in data:
            # Get the convoy... this should not fail since we can't reconstruct it from
            # the data in this file
            cur.execute("SELECT convoy_pk FROM convoys WHERE request_id=%s",(r['transport request #'],))
            convoy_pk = cur.fetchone()[0]
            
            # Get the vehicles. Treat their ID like an asset_tag and upsert
            vehicle_pks = list()
            for v in r['assigned vehicles'].split(','):
                v = v.strip()
                vehicle_pks.append(vehicle_upsert(v))
            
            # Upsert the used_by records
            for v in vehicle_pks:
                used_upsert(v, convoy_pk)
                
            # Insert the waypoints, time format seems pretty consistent and this is the 
            # only source of waypoint information
            if not r['waypoint1 time'] == '':
                ts = parse_time(r['waypoint1 time']).isoformat()
                cur.execute("INSERT INTO waypoints (convoy_fk,point_dt) VALUES (%s,%s)",(convoy_pk,ts))
            if not r['waypoint 2 time'] == '':
                ts = parse_time(r['waypoint 2 time']).isoformat()
                cur.execute("INSERT INTO waypoints (convoy_fk,point_dt) VALUES (%s,%s)",(convoy_pk,ts))
            if not r['waypoint 3 time'] == '':
                ts = parse_time(r['waypoint 3 time']).isoformat()
                cur.execute("INSERT INTO waypoints (convoy_fk,point_dt) VALUES (%s,%s)",(convoy_pk,ts))
            if not r['waypoint 4 time'] == '':
                ts = parse_time(r['waypoint 4 time']).isoformat()
                cur.execute("INSERT INTO waypoints (convoy_fk,point_dt) VALUES (%s,%s)",(convoy_pk,ts))

def main():
    process_waypoints()
    conn.commit()

if __name__=='__main__':
    main()