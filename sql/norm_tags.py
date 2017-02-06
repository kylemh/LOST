# This script deals with multiple asset tags in a row

import csv

def process_transit(outf):
    outf.write("asset tag,src facility,dst facility,depart date,arrive date,transport request #,Comments\n")
    with open('osnap_legacy/transit.csv') as f:
        data = csv.DictReader(f)
        for r in data:
            ats = r['asset tag'].split(',')
            for a in ats:
                outf.write('%s,"%s","%s",%s,%s,%s,%s\n'%(a.strip(),r['src facility'],r['dst facility'],r['depart date'],r['arrive date'],r['transport request #'],r['Comments']))

def main():
    with open('transit.csv','w') as f:
        process_transit(f)

if __name__=='__main__':
    main()