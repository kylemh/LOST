# Open the product file and generate a load file

import csv

def process_products(outf):
    with open('osnap_legacy/product_list.csv') as f:
        data = csv.DictReader(f)
        for r in data:
            for k in r.keys():
                print("%s: %s"%(k,r[k]))
                if r[k]=='':
                    r[k]='NULL'
                elif k=='unit price':
                    pass
                else:
                    r[k]="'%s'"%r[k] # if single quotes are in the data this will fail
                    
            # Add the product entry
            outf.write("INSERT INTO products (vendor,product_name,product_model,description,price) VALUES (%s,%s,%s,%s,%s);\n"%(r['vendor'],r['name'],r['model'],r['description'],r['unit price']))
            
            # Add the security tag if there is one
            if not r['compartments']=='NULL':
                (tc,tl) = r['compartments'].split(':')
                # This query exploits how serial values are generated and may fail
                # if something else is running at the same time as the migration script.
                # This query is also likely to be super inefficient for large migrations.
                outf.write("INSERT INTO security_tags (level_fk, compartment_fk, product_fk) SELECT level_pk, compartment_pk, max(product_pk) FROM sec_levels l,sec_compartments c,products p WHERE l.abbrv='%s and c.abbrv=%s' GROUP BY level_pk,compartment_pk,product_pk;\n"%(tl,tc))

def main():
    with open('prod_load.sql','w') as f:
        process_products(f)

if __name__=='__main__':
    main()
