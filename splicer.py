#Elimina nts de un fasta de reads desde una posicion de inicio dada por BLAST

#!/usr/bin/python

import sys, linecache

blast_file=sys.argv[1]
reads_file=sys.argv[2]

n=0
step=2
for x in open(blast_file):
    line=" ".join(x.split())
    name=line.split(" ")[0]
    end=int(line.split(" ")[9])
    n+=step
    seq=linecache.getline(sys.argv[2],n)
    seqnext=linecache.getline(sys.argv[2],n+1)
    if seqnext[:1] != ">":
        seq=seq.rstrip()+seqnext.rstrip()
        step = 3
    else:
        step=2
    out= ">"+name+"\n"+seq[end:].rstrip()
    print out
