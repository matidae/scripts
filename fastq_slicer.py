#Splitea nts del final de un read de archivos fastq
import sys
from HTSeq import FastqReader

infile=sys.argv[1]
nts=int(sys.argv[2])
fastq=FastqReader(infile,'solexa')
aux=''

for read in fastq:
	aux+=read.name+'\n'+read.seq[:nts]+'\n'

outfile=open(infile+'_salida','w')
outfile.write(aux)
