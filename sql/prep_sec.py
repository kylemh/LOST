# Open the security csv files and generate a load file

import csv

def process_levels(outf):
    with open('osnap_legacy/security_levels.csv') as f:
        data = csv.DictReader(f)
        i = 5
        for r in data:
            outf.write("INSERT INTO sec_levels (level_pk,abbrv,comment) VALUES (%s,'%s','%s');\n"%(i,r['level'],r['description']))
            i = i-1

def process_compartments(outf):
    with open('osnap_legacy/security_compartments.csv') as f:
        data = csv.DictReader(f)
        for r in data:
            outf.write("INSERT INTO sec_compartments (abbrv,comment) VALUES ('%s','%s');\n"%(r['compartment_tag'],r['compartment_desc']))

def main():
    with open('sec_load.sql','w') as f:
        process_levels(f)
        process_compartments(f)

if __name__=='__main__':
    main()