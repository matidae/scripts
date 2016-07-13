#!/usr/bin/env python
import sys
import re


def process_nuc(ref, base_list):
    base_list_new = []
    base_list = base_list.replace(".", ref).replace(",", ref).\
                replace("*", "").upper()
    indels = set(re.findall("\d+", base_list))
    indels = "|".join([".."+i+".{"+i+"}" for i in indels])
    base_list = re.sub('\^.(.)', lambda x: x.expand(r'\1').lower(), base_list)
    base_list = re.sub('(.)\$', lambda x: x.expand(r'\1').lower(), base_list)
    indels_new = map(lambda x: x.upper(), re.findall(indels, base_list))
    indels_new_aux = []
    for i in indels_new:
        if len(i) > 0:
            indels_new_aux.append(i)
    base_list = list(re.sub(indels, '', base_list))
    return base_list + indels_new_aux


def sort_list(proc_list):
    data = set(proc_list)
    sort_list_aux = [(i, proc_list.count(i)) for i in data]
    return sorted(sort_list_aux, key=lambda x: x[1], reverse=True)


def main(pileup_file):
    with open(sys.argv[1]) as pileup:
        for entry in pileup:
            pos = entry.split()[1]
            ref = entry.split()[2]
            base_list = entry.split()[4]
            proc_list = process_nuc(ref, base_list)
            sorted_list = sort_list(proc_list)
            print pos, ref, sorted_list

if __name__ == "__main__":
    pileup_file = sys.argv[1]
    main(pileup_file)
