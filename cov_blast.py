import sys
import subprocess
import re

lista = [i.strip() for i in open(sys.argv[1])]

for i in lista:
    name = i.split()[1].strip()
    length = int(i.split()[0])
    vec = [0]*length
    proc = subprocess.Popen(['grep', '-w', name, sys.argv[2]], stdout=subprocess.PIPE)
    out = proc.stdout.read().split("\n")
    for j in out:
        if len(j)>0:
            start = int(j.split("\t")[8]) if int(j.split("\t")[8]) < int(j.split("\t")[9]) else int(j.split("\t")[9]) 
            end  = int(j.split("\t")[9]) if int(j.split("\t")[8]) < int(j.split("\t")[9]) else int(j.split("\t")[8]) 
            for k in xrange(start -1, end):
                vec[k]=1
    vector = "".join(map(str, vec))
    search = re.finditer("11*", vector)
    pos = [(i.start(0)+1, i.end(0)) for i in search]
    posvec=[]
    if len(pos) != 0:
        if len(pos) == 1 and  pos[0][1] - pos[0][0] >= 100:
            print name, pos[0][0], pos[0][1]
        else:
            saux = pos[0][0]
            for i in xrange(1, len(pos)):
                eaux = pos[i-1][1]
                if pos[i][0] - eaux  < 30:
                    eaux = pos[i][1]
                else:
                    if eaux - saux >= 100:
                        posvec.append((saux, eaux))
                    saux = pos[i][0]
                    eaux = pos[i][1] 
        
            for i in posvec:
                print name, i[0], i[1]
