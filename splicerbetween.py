#Se quenda con los nts de un fasta de reads entre posiciones de inicio 
#y fin dadas por la salida m8 de BLAST

#!/usr/bin/python

import sys, linecache

blast_file=sys.argv[1]
reads_file=sys.argv[2]
n=0
step=2
for x in open(blast_file):
    line=" ".join(x.split())
    name=line.split(" ")[0]
    start=int(line.split(" ")[6])
    end=int(line.split(" ")[7])
    n+=step
    seq=linecache.getline(sys.argv[2],n)
    seqnext=linecache.getline(sys.argv[2],n+1)
    if seqnext[:1] != ">":
        seq=seq.rstrip()+seqnext.rstrip()
        step = 3
    else:
        step=2
    out= ">"+name+"\n"+seq[start-1:end-1].rstrip()
    print out

