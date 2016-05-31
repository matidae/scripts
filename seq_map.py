#!/usr/bin/env python
import sys

with open(sys.argv[1]) as pileup:
    for entry in pileup:
        nuc_ref = entry.split()[2]
        mapping = entry.split()[4]
        mapping.replace(".", nuc_ref).replace(",", nuc_ref)
        countA = nt_map.count("A")
        countT = nt_map.count("T")
        countG = nt_map.count("G")
        countC = nt_map.count("C") 

