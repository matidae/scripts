#!/usr/bin/env python
import sys, re

def process_nuc(ref, base_list):
    base_list_new = []
    c = 1
    while c < len(base_list):
        if (base_list[c] == "-" or  base_list[c] == "+") and \
        base_list[c-1] != "^":
            indel_len = ''
            for i in base_list[c+1]:
                if '0' <= i <= '9':
                    indel_len += i
                else:
                    break
            indel_len = int(indel_len)
            indel_base = base_list[c-1 : c+indel_len+2] \
                        .replace(".", ref).replace(",", ref)
            base_list_new.append(indel_base.upper())
            c += indel_len + 3
        elif base_list[c-1] == "^":
            c+= 2
        elif base_list[c-1] == "$" or base_list[c-1] == "*":
            c += 1
        elif base_list[c-1] == "." or base_list[c-1] == ",":
            base_list_new.append(ref.upper())
            c += 1
        else:
            base_list_new.append(base_list[c-1].upper())
            c += 1
    return base_list_new        


def process_qual(qual_list):
    qual_list_new = []
    for qual in qual_list:
        qual_list_new.append(ord(qual))
    return qual_list_new


def filter_by_qual(base_list_new, qual_list_new):
    c = 0
    base_list_filtered = []
    qual_list_filtered = []
    for base, qual in zip(base_list_new, qual_list_new):
        if qual >= 20:
            base_list_filtered.append(base)
            qual_list_filtered.append(qual)
    return base_list_filtered


def get_base(ref, base_list_filtered):
    base_set = list(set(base_list_filtered))
    base_count = []
    for base in base_set:
        base_count.append(base_list_filtered.count(base))
    if sum(base_count) > 0:
        seq = base_set[base_count.index(max(base_count))]
        max_count = max(base_count)
        return (seq, max_count)
    else:
        return (ref, 0)


def is_indel(seq, c, indel_len):
    for_indel = seq[c][1]
    not_indel = 0    
    for i in xrange(indel_len):
        not_indel += seq[c+i+1][1]
    return for_indel > not_indel


def process_seq(seq, name):
    final_seq = ""
    for c in xrange(len(seq)):
        if "-" in seq[c][0]: # or "+" in seq[c][0]:
            indel_len = int(re.findall('\d+', seq[c][0])[0])
            indel = is_indel(seq, c, indel_len)
            if indel:
#                if seq[c][0] == "+":
#                    final_seq += "".join(re.findall('[A-Z]',seq[c][0]))
#                else:
                final_seq += seq[c][0][0]
                c += indel_len
        elif "+" in seq[c][0]:
            final_seq += "".join(re.findall('[A-Z]',seq[c][0]))
        else:
            final_seq += seq[c][0]
#        print c, seq[c]
#    print ">" + name 
#    print final_seq

def main(pileup_file):
    with open(sys.argv[1]) as pileup:
        seq = []
        for entry in pileup:
            name = entry.split()[0]
            ref = entry.split()[2].lower()
            depth = int(entry.split()[3])
            if depth > 0:
                base_list = entry.split()[4]
                qual_list = entry.split()[5]
                base_list_new = process_nuc(ref, base_list)
                qual_list_new = process_qual(qual_list)
                base_list_filtered = filter_by_qual(base_list_new, qual_list_new)
                seq_aux = get_base(ref, base_list_filtered)
                seq.append(seq_aux)
                print base_list_new
            else:
                seq.append((ref, 0))
        n=1
#        for i in seq:
#            print n,i
#            n+=1
        process_seq(seq, name)

if __name__ == "__main__":
    pileup_file = sys.argv[1]
    main(pileup_file)

