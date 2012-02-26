#!/usr/bin/python
import sys
from math import floor, ceil

num_lines = sum(1 for line in open(sys.argv[1]))
nline = 0
bed_file = open(sys.argv[1],'r')
block = []
block_number = 0
chr_aux=""
strand_aux=""

for line in bed_file:
    nline+=1
    strand = line.split("\t")[5].rstrip()
    chr = line.split("\t")[0]
    if strand == "+":
        start = int(line.split("\t")[1])
    else:
        start = int(line.split("\t")[2])
    if block:
        favg = float(sum(block))/float(len(block))
        avg=int(floor(favg)) if str(favg).split(".")[1][:2]<50 else int(ceil(favg))
        if start<avg+3 and start>avg-3:
            block.append(start)
            chr_aux=chr
            strand_aux=strand
        else:
            block_number+=1
            print "block"+str(block_number)+"\t"+str(avg)+"\t"+str(len(block))+"\t"+strand+"\t"+chr_aux
            block = []
            block.append(start)
            chr_aux=chr
            strand_aux=strand
        if nline==num_lines:
            block_number+=1
            avg = sum(block)/len(block)
            print "block"+str(block_number)+"\t"+str(avg)+"\t"+str(len(block))+"\t"+strand+"\t"+chr_aux
    else:
        block.append(start)
        chr_aux=chr
        strand_aux=strand
bed_file.close()
