#Uso python ortalign.py nombre_ortologos ort1.fasta ort2.fasta ort3.fasta
#Toma un archivo de 3 columna de nombres de genes ortologos
#los busca en los fasta y los alinea de a 3 con clustalw

import sys
from Bio import SeqIO
from subprocess import call

ort_file = open(sys.argv[1], "r")

ort = [line.rsplit() for line in open(sys.argv[1], "r")]
n=0

for i in ort:
   out = open(str(n)+".fas","w")
   for seq1 in SeqIO.parse(sys.argv[2], "fasta"):
      if seq1.id == i[0]: 
         SeqIO.write(seq1, out, "fasta")
   for seq2 in SeqIO.parse(sys.argv[3], "fasta"):
      if seq2.id == i[1]:
         SeqIO.write(seq2, out, "fasta")
   for seq3 in SeqIO.parse(sys.argv[4], "fasta"):
      if seq3.id == i[2]:
         SeqIO.write(seq3, out, "fasta")

   out.close()
   call(["clustalw",str(n)+".fas"])
   call(["rm",str(n)+".fas"])
   call(["rm",str(n)+".dnd"])
   n+=1 
