#!/usr/bin/env python
import sys
from Bio import SeqIO

data = SeqIO.index(sys.argv[1], "fasta")

with open(sys.argv[2]) as lista:
    for i in lista:
        print data[i.rstrip()].format("fasta")
