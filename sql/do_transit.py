import psycopg2
import sys
import csv
import re
import datetime

def normalize_date(s):
    m = re.match(r'(\d+)/(\d+)/(\d+)',s)
    if m:
        # slash style
        mon = int(m.group(1))
        day = int(m.group(2))
        yr  = int(m.group(3))
        if yr < 100: # short year
            if yr < 50: # assume current century
                yr += 2000
            else: # assume last century
                yr += 1900
        return datetime.datetime(yr,mon,day)
        
    m = re.match(r'(\d+)-(\w{3})-(\d+)',s)
    if m:
        # full abbrv style
        day = int(m.group(1))
        mon = MONTH[m.group(2)]
        yr = int(m.group(3))
        if yr < 100: # short year
            if yr < 50: # assume current century
                yr += 2000
            else: # assume last century
                yr += 1900
        return datetime.datetime(yr,mon,day)
    m = re.match(r'(\w{3})-(\d+)',s)
    if m:
        # short abbrv style... Mon-DD?
        # These have ambiguous years. Assume the most recent past
        day = int(m.group(2))
        mon = MONTH[m.group(1)]
        now = datetime.datetime.utcnow()
        ret = datetime.datetime(now.year,mon,day)
        if ret > now:
            ret = datetime.datetime(now.year-1,mon,day)
        return ret

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def asset_upsert(asset_tag):
    cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("INSERT INTO assets (asset_tag) VALUES (%s)",(asset_tag,))
    cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
    return cur.fetchone()[0]

def ffind(fname):
    # Manual mapping in code... should be in a dict or lookup table
    if fname=='MB 005':
        fname='Moonbase'
    if fname=='Los Alamous, NM':
        fname='Los Alamos, NM'
    if fname=='Las Alamos, NM':
        fname='Los Alamos, NM'
    if fname=='Washington, D.C.':
        fname='Washington, DC'
        
    cur.execute("SELECT facility_pk FROM facilities WHERE common_name=%s",(fname,))
    r = cur.fetchone()
    if r:
        return r[0]
    raise Exception("Bad facility name %s"%fname)
    
def convoy_upsert(req, src_pk, dst_pk, load_dt, unload_dt):
    cur.execute("SELECT convoy_pk FROM convoys WHERE request_id=%s",(req,))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("INSERT INTO convoys (request_id,src_fk,dst_fk,depart_dt,arrive_dt) VALUES (%s,%s,%s,%s,%s)",(req,src_pk,dst_pk,load_dt,unload_dt))
    cur.execute("SELECT convoy_pk FROM convoys WHERE request_id=%s",(req,))
    return cur.fetchone()[0]

def on_insert(asset_pk,convoy_pk,load_dt,unload_dt):
    cur.execute("SELECT count(*) FROM asset_on WHERE asset_fk=%s and convoy_fk=%s",(asset_pk,convoy_pk))
    r = cur.fetchone()
    if r[0] > 0:
        raise Exception("Duplicated data?")
    cur.execute("INSERT INTO asset_on (asset_fk,convoy_fk,load_dt,unload_dt) VALUES (%s,%s,%s,%s)",(asset_pk,convoy_pk,load_dt,unload_dt))
    
def process_transit():
    # I'm going to ignore the comment field... 
    with open('transit.csv') as f:
        data = csv.DictReader(f)
        for r in data:
            # check if the asset exists and get the pk
            asset_pk = asset_upsert(r['asset tag'])
            # attempt to map the facilities to fcodes
            src_pk = ffind(r['src facility'])
            dst_pk = ffind(r['dst facility'])
            # normalize dates
            load_dt = normalize_date(r['depart date'])
            unload_dt = normalize_date(r['arrive date'])
            # check if the convoy existis and get the pk
            convoy_pk = convoy_upsert(r['transport request #'],src_pk,dst_pk,load_dt,unload_dt)
            # add asset_on record
            on_insert(asset_pk,convoy_pk,load_dt,unload_dt)
    conn.commit()
    
def main():
    process_transit()

if __name__=='__main__':
    main()