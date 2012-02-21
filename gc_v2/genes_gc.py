#Uso python genes_gc.py codones expresion
#Devuelve niveles de contenido de GC y expresion p/c/gen

import sys
file_cod=open(sys.argv[1],"r")
gc_content=[]
for i in file_cod:
    j=i.split(",")
    total=sum(int(x) for x in j)
    gc=sum(int(j[x]) for x in range(0, len(j)) if x%2!=0 )
    gc_content.append(gc/float(total))
file_cod.close()

gc_out=[]; n=0;
file_exp=open(sys.argv[2],"r")
for i in file_exp: 
    gc_out.append(i.rstrip()+"\t"+str(gc_content[n])); 
    n+=1;
file_exp.close()

file_out=open(sys.argv[2]+"_gc","w")
for i in gc_out: file_out.write("%s\n" % i)
file_out.close()
