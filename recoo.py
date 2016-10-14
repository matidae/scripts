import sys

fixes = {line.split()[0].strip():map(int,line.split()[1].split(',')) for line in open(sys.argv[1])}
outfile = open(sys.argv[3],'w')
with open(sys.argv[2]) as fh:
    for i in fh:
     try:
        coor = pre = name = ""
        if len(i.split()) == 7:
            coor = i.split()[6]
            pre = " ".join(i.split()[:6])
        else:
            coor = i.split()[5]
            pre = " ".join(i.split()[:4])
        name = i.split()[3]
        if name.count("_") == 1:
            name = name.split('_')[0]
        elif name.count("_") == 2:
            name = "_".join(name.split("_")[:1])
        vec_coor = fixes[name]
        coor = coor.replace('<','').replace('>','').replace(':',',').split(',')
        first = True
        line = ""
        start = 0 
        for j in coor:
            if first:
                line += str(int(j) + sum(vec_coor[:int(j)])) + ':'
                first = False
            else:
                line += str(int(j) + sum(vec_coor[:int(j)])) + ','
                first = True
        outfile.write( pre + ' ' + line[:-1] + '\n')
     except:
        pass
outfile.close()
