import sys

gene_dict = {}
with open(sys.argv[2]) as fh:
    for i in fh:
        key = i.split()[1]
        if key == 'gene':
            name = i.split()[3].split('_')[0]
            start = int(i.split()[4].replace('>','').replace('<',''))
            gene_dict[name] = start

with open(sys.argv[1]) as fh:
    for i in fh:
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
        coor = coor.replace('>','').replace('<','').replace(':',',').split(',')
        gene_start = gene_dict[name]
        first = pair = False
        line = ""
        start = 0
        for j in coor:
            if pair:
                pos = int(j) - gene_start + 200 + 1 
                line += str(pos) + ","
                pair = False
            else:
                pos = int(j) - gene_start + 200 + 1
                line += str(pos) + ":"
                pair = True
        print pre + " " + line[:-1]
