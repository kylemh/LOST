import csv
import sys
import re
import datetime

MONTH = { 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12 }

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

def process_tag(tagval,asset_tag):
    tagval = tagval.strip()
    (tc,tl) = tagval.split(":")
    return "INSERT into security_tags (level_fk, compartment_fk, asset_fk) SELECT level_pk, compartment_pk, asset_pk FROM sec_levels l,sec_compartments c,assets a WHERE l.abbrv='%s' and c.abbrv='%s' and a.asset_tag=%s;\n"%(tl,tc,asset_tag)
    
def process_inventory(outf,inf):
    with open(inf) as f:
        data = csv.DictReader(f)
        for r in data:
            # Normalize date
            if not r['intake date']=='':
                r['intake date'] = normalize_date(r['intake date']).isoformat()
            if not r['expunged date']=='':
                r['expunged date'] = normalize_date(r['expunged date']).isoformat()
            # Prep for query gen
            for k in r.keys():
                if k=='compartments':
                    pass
                elif r[k]=='':
                    r[k]='NULL'
                else:
                    r[k]="'%s'"%r[k] # if single quotes are in the data this will fail

            # Add the asset, use product as description
            outf.write("INSERT INTO assets (asset_tag,description) VALUES (%s,%s);\n"%(r['asset tag'],r['product']))
            # Attach the asset to the facility
            #   Will fail if there is no preexisting facility record
            outf.write("INSERT INTO asset_at (asset_fk,facility_fk,arrive_dt,depart_dt) SELECT asset_pk,facility_pk,%s,%s FROM assets a, facilities f WHERE a.asset_tag=%s and f.fcode=%s;\n"%(r['intake date'],r['expunged date'],r['asset tag'],r['fcode']))
            # Attach the asset to its tags
            if not r['compartments']=='':
                for t in r['compartments'].split(','):
                    outf.write(process_tag(t,r['asset tag']))
        
        # Add product_fks if there is something sensible to add
        outf.write("UPDATE assets SET product_fk=product_pk FROM products p WHERE assets.description=p.product_name;\n")

def main():
    with open('inv_load.sql','w') as f:
        process_inventory(f,sys.argv[1])

if __name__=='__main__':
    main()
