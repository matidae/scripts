#!/usr/bin/env python
import sys, re
from Bio import SeqIO

def process_nuc(ref, base_list):
    base_list_new = []
    c = 1
    start_flag = False
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
            start_flag = True
        elif base_list[c-1] == "$" or base_list[c-1] == "*":
            c += 1
            base_list_new[:-1] + base_list_new[-1].lower()
        elif base_list[c-1] == "." or base_list[c-1] == ",":
            base_list_new.append(ref.upper())
            c += 1
        else:
            if border_flag:
                base_list_new.append(base_list[c-1].lower())
            else:
                base_list_new.append(base_list[c-1].upper())
            start_flag = False
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


def is_del(seq, c, del_len):
    for_del = seq[c][1]
    not_del = 0    
    for i in xrange(del_len):
        not_del += seq[c+i+1][1]
    return for_del > not_del


def process_seq(seq, name):
    final_seq = ""
    c = 0
    while c < len(seq):
        if "-" in seq[c][0]:
            del_len = int(re.findall('\d+', seq[c][0])[0])
            isdel = is_del(seq, c, del_len)
            if isdel:
                final_seq += seq[c][0][0]
                c += del_len +1
            else:
                final_seq += seq[c][0][0]
                c += 1
        elif "+" in seq[c][0]:
            final_seq += "".join(re.findall('[A-Z]',seq[c][0]))
            c += 1
        else:
            final_seq += seq[c][0]
            c += 1
    print ">" + name 
    print final_seq

def parse_entry(entry):
    ref = entry.split()[2].lower()
    depth = int(entry.split()[3])
    if depth > 0:
        base_list = entry.split()[4]
        qual_list = entry.split()[5]
        base_list_new = process_nuc(ref, base_list)
        qual_list_new = process_qual(qual_list)
        base_list_filtered = filter_by_qual(base_list_new, qual_list_new)
        seq_aux = get_base(ref, base_list_filtered)
        return seq_aux
    else:
        return (ref, 0)
    
def main(pileup_file, fasta_file):
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = []
        fasta_name = record.id
        fasta_seq = str(record.seq)
        count = 1 
        with open(sys.argv[1]) as pileup:
            for entry in pileup:
                name = entry.split()[0]
                if fasta_name == name:
                    pos = int(entry.split()[1])
                    if count == pos:
                        seq.append(parse_entry(entry))
                        count += 1
                    else:
                        while count < pos:
                            seq.append((fasta_seq[count -1], 0))
                            count += 1
                        seq.append(parse_entry(entry))
                        count += 1 
        process_seq(seq, name)

if __name__ == "__main__":
    pileup_file = sys.argv[1]
    fasta_file = sys.argv[2]
    main(pileup_file, fasta_file)

