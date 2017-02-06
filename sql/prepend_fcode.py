# This script concatenates and prepends some data for inventory files

import sys
import re
from pathlib import Path

def process_file(fname):
    p = Path(fname)
    name = p.name
    m = re.match('([^_]+)_inventory.csv',name)
    if not m:
        return
    with p.open() as f:
        f.readline()
        for line in f:
            line = line.strip()
            print("%s,%s"%(m.group(1),line))
    

def main():
    print("fcode,asset tag,product,room,compartments,intake date,expunged date")
    for arg in sys.argv[1:]:
        process_file(arg)
        
if __name__=='__main__':
    main()