import sys

temp_name = ""
poly_prop = 0
nt_pos = {"A":0, "T":1, "G":2, "C":3}
nt_pos_rev = {0:"A", 1:"T", 2:"G", 3:"C"}

if len(sys.argv) > 2:
    try:
        poly_prop = float(sys.argv[2])/100
    except:
        pass

def init_matrix():
    return [[0]*4 for i in xrange(4)]

def count(sub_matrix, n_line):
    nt_ref = n_line.split()[2]
    if int(n_line.split()[3]) > 0 :
        nt_map = n_line.split()[4].replace(".", nt_ref).replace(",", nt_ref).upper()
        countA = nt_map.count("A")
        countT = nt_map.count("T")
        countG = nt_map.count("G")
        countC = nt_map.count("C")
        if nt_ref in ["A", "T", "G", "C"]:
            if nt_map.count(nt_ref) > 0:
                if float(nt_map.count(nt_ref))/(countA + countC + countG + countT) >= poly_prop:
                    sub_matrix[nt_pos[nt_ref]][nt_pos["A"]] += countA
                    sub_matrix[nt_pos[nt_ref]][nt_pos["T"]] += countT
                    sub_matrix[nt_pos[nt_ref]][nt_pos["G"]] += countG
                    sub_matrix[nt_pos[nt_ref]][nt_pos["C"]] += countC
    return sub_matrix

def prop_matrix(sub_matrix):
    p_matrix = [[0]*4 for i in xrange(4)]
    x = y = 0
    for row in sub_matrix:
        row_total = sum(row)
        for item in row:
            if item > 0:
                p_matrix[x][y] = float(item)/row_total
            else:
                p_matrix[x][y] = 0
            y += 1
        x += 1
        y = 0
    return p_matrix 

def count_error(prop_matrix):
    error_rate = 0
    for x in xrange(1, len(prop_matrix)):
        for y in xrange(1, len(prop_matrix[x])):
            if x != y :
                error_rate += prop_matrix[x][y]
    return error_rate        

def print_matrix(name, sub_matrix):
    p_matrix = prop_matrix(sub_matrix)
    print name
    print str(" "*5).join(["","A","T","G","C"])
    n = 0
    for i,j in zip(p_matrix, sub_matrix):
        print " ".join([nt_pos_rev[n]] + map("{0:.5f}".format,i)), "\t", j
        n += 1
    print "\t"*5 + "error rate: " + "{0:.3f}".format(count_error(p_matrix)*100) + "%"

with open(sys.argv[1]) as fh:
    for i in fh:
        name = i.split()[0]
        if temp_name == "":
            sub_matrix = init_matrix()
            temp_name = name        
            n_line = i.rstrip()
            sub_matrix = count(sub_matrix, n_line)
        elif temp_name == name:
            n_line = i.rstrip()
            sub_matrix = count(sub_matrix, n_line)
        else:
            print_matrix(temp_name, sub_matrix)
            temp_name = name
            sub_matrix = init_matrix()
            n_line = i.rstrip()
            sub_matrix = count(sub_matrix, n_line)
        
print_matrix(name, sub_matrix)
