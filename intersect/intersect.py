#!/usr/bin/python
import sys

gff_file = open(sys.argv[1],'r')
genes = []
blocks_file = open(sys.argv[2],'r')

for line in gff_file:
   start = int(line.split("\t")[3])
   end = int(line.split("\t")[4])
   strand = line.split("\t")[6]
   name = line.split("=")[2].split(";")[0]
   desc = line.split("=")[3].split(";")[0]
   chr = line.split("\t")[0]
   genes.append([start, end, strand, name +";"+ desc, chr])

for line in blocks_file:
   pos = int(line.split("\t")[1])
   strand = line.split("\t")[3]
   chr = line.split("\t")[4].rstrip()
   for g in genes:
      if pos>g[0] and pos<g[1] and chr==g[4]:
          print line.rstrip()+"\t"+str(g[0])+"\t"+str(g[1])+"\t"+g[3]

