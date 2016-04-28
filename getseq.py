#!/usr/bin/env python
import sys
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("fasta", help="Fasta file")
parser.add_argument("seqs", help="File with sequence names or comma separated sequence names")
parser.add_argument("-u", help="Print each sequence in a single line", action="store_true")
args = parser.parse_args()

fasta = args.fasta
data = SeqIO.index(fasta, "fasta")
seqs = args.seqs
with open(seqs) as listseq:
    for i in listseq:
        if args.u:
            print ">" + i.rstrip()
            n = 0
            seq = data[i.rstrip()].seq
            for j in xrange(0, len(seq)/60 + 1):
                print seq[n:n+60]
                n+=60
        else:
            print data[i.rstrip()].format("fasta")
