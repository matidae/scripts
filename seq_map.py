#!/usr/bin/env python
import sys

def process_nuc(ref, base_list):
    base_list_new = []
    c = 0
    while c < len(base_list):
        if base_list[c] == "." or base_list[c] == ",":
            base_list_new.append(ref)
            c += 1
        elif base_list[c] == "^":
            c += 2
        elif base_list[c] == "+" or base_list[c] == "-":
            indel_len = int(base_list[c+1])
            indel_mod = base_list[c : c+indel_len+2]
            base_list_new.append(indel_mod)
            c += indel_len+2
        else:
            base_list_new.append(base_list[c])
            c += 1
    return base_list_new


def process_qual(qual_list):
    qual_list_new = []
    for qual in qual_list:
        qual_list_new.append(ord(qual))
    return qual_list_new

"""
def weight_base(base_list_new, qual_list_new):
    base_set = set(base_list_new)
    base_weigth = {k:0 for k in base_set}
    qual_total = sum(qual_list_new)
    for base, qual in zip(base_list_new, qual_list_new):
        base_weigth[base] += qual/(qual_total * 1.0)
    return base_weigth

def process_base_weight(base_weight):
    print base_weight
"""
def filter_by_qual(base_list_new, qual_list_new):
    c = 0
    base_list_filtered = []
    qual_list_filtered = []
    for base, qual in zip(base_list_new, qual_list_new):
        if qual >= 20:
            base_list_filtered.append(base)
            qual_list_filtered.append(qual)
    return base_list_filtered


def print_base(ref, base_list_filtered):
    base_set = list(set(base_list_filtered))
    print base_set
    base_count = []
    for base in base_set:
        base_count.append(base_list_filtered.count(base))
    if sum(base_count) > 0:
        seq = base_set[base_count.index(max(base_count))]
        if "+" in seq:
            return seq[2:]
        elif "-" in seq:
            return 
        else:
            return seq
    else:
        return ref.lower()

def main(pileup_file):
    with open(sys.argv[1]) as pileup:
        seq = ""
        for entry in pileup:
            ref = entry.split()[2]
            base_list = entry.split()[4]
            qual_list = entry.split()[5]
            base_list_new = process_nuc(ref, base_list.upper())
            qual_list_new = process_qual(qual_list)
          #  base_weight = weight_base(base_list_new, qual_list_new)
          #  process_base_weight(base_weight)
            filtered_data = filter_by_qual(base_list_new, qual_list_new)
            base_list_filtered = filtered_data
          #  qual_list_filtered = filtered_data[1]
            seq_aux = print_base(ref, base_list_filtered)
            if seq_aux:
                seq += seq_aux
        print seq

if __name__ == "__main__":
    pileup_file = sys.argv[1]
    main(pileup_file)

