#!/usr/bin/env python
import sys
import argparse
import os.path
from Bio import SeqIO

def printSixty(seq):
    n = 0
    sixty = []
    for i in xrange(0, len(seq)/60+1):
        sixty.append(seq[n:n+60])
        n += 60
    return sixty

def oneline(seq):
    if args.u:
        return seq
    else:
        return printSixty(seq)

def rev(seq):
    if args.r:
        return seq.reverse_complement()
    else:
        return seq

def printSeq(seq):
    if type(seq) == list:
        for i in seq:
            print i
    else:
        print seq

parser = argparse.ArgumentParser()
parser.add_argument("fasta", help="Fasta file", nargs="?")
parser.add_argument("seqs", help="File with sequence names or comma separated sequence names (e.g 'list.txt' or 'gene1,gene2,gene3')", nargs="?", default="-")
parser.add_argument("-u", help="Print each sequence in a single line (default: 60 chars per line)", action="store_true")
parser.add_argument("-r", help="Print reverse complement sequence", action="store_true")
parser.add_argument("-l", help="Print length and name of a sequence", action="store_true")
args = parser.parse_args()

if args.fasta == None:
    parser.print_help()
    sys.exit()

if "-" not in args.seqs:
    data = SeqIO.index(args.fasta, "fasta")
    if os.path.isfile(args.seqs):
        with open(args.seqs) as listseq:
            for i in listseq:
                if args.l:
                    print "\t".join(map(str,[len(data[i.rstrip()].seq),i.rstrip()]))
                else:
                    print ">" + i.rstrip()
                    seq = oneline(rev(data[i.rstrip()].seq))
                    printSeq(seq)
    else:
        seqs = args.seqs.split(",")
        for i in seqs:
            if args.l:
                print "\t".join(map(str,[len(data[i.rstrip()].seq),i.rstrip()]))
            else:
                print ">" + i.rstrip()
                seq = oneline(rev(data[i.rstrip()].seq))
                printSeq(seq)
else:
    for i in SeqIO.parse(args.fasta, "fasta"):
        if args.l:
            print "\t".join(map(str,[len(i.seq),i.id]))
        else:
            print ">" + i.id
            seq = oneline(rev(i.seq))
            printSeq(seq)
