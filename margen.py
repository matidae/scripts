import sys, os, re
from Bio import SeqIO

gff_file = open(sys.argv[1], "r")
#list_file = open(sys.argv[2], "r")
gen = sys.argv[2]
margen = int(sys.argv[3])

chrom = start = end = strand = ""

def getChromosomes():
   chromo_list=[]
   gff_file = open (sys.argv[1], "r")
   for line in gff_file:
      if "##sequence-region" in line:
         chromo_list.append(line.split("\t")[1])
   return chromo_list

def fastaChromosomes():
   flag = False
   chromo_list = getChromosomes()
   gff_file = open (sys.argv[1], "r")
   chromo_file = open (sys.argv[1]+".chr.fasta", "w")
   for line in gff_file:
      if flag:
         chromo_file.write(line)
      if ">"+chromo_list[0] in line:
         print chromo_file.write(line)
         flag = True

if not os.path.isfile(sys.argv[1]+".chr.fasta"):
   fastaChromosomes()   

#for i in list_file:
def printGene():
   #gen = i.rsplit()
   for line in gff_file:
      if line[0]!="#":
         if (re.findall("\\b"+gen+"\\b",line)) and line.split("\t")[2] == "gene":
            vector = line.split("\t")
            chrom = vector[0]
            start = vector[3]
            end = vector[4]
            strand = vector[6]
            break

   for i in SeqIO.parse(sys.argv[1]+".chr.fasta", "fasta"):
      if i.id == chrom:
          if strand == "+":
             print ">"+gen +"\t"
             print i.seq[int(start) - 1 - margen : int(end)]
          else:
             print ">"+gen +"\t"
             seq = i.seq[int(start) - 1 : int(end) + margen] 
             print seq.reverse_complement()
printGene()
