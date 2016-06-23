#!/usr/bin/env python
import sys
import re
from Bio import SeqIO


def process_nuc(ref, base_list):
    """Parsea una entrada de mapeo del pileup a un formato mas legible.
    Input: base de referencia, lista de bases mapeadas en formato CIGAR.
    Output: lista de bases para cada posicion
    """
    base_list_new = []
    c = 1
    start_flag = False
    while c < len(base_list):
        if (base_list[c] == "-" or base_list[c] == "+") and \
        base_list[c-1] != "^":
            indel_len = ''
            for i in base_list[c+1:c+3]:
                if '0' <= i <= '9':
                    indel_len += i
                else:
                    break
            indel_len = int(indel_len)
            indel_base = base_list[c-1: c+indel_len+2].replace(".", ref).\
            replace(",", ref)
            base_list_new.append(indel_base.upper())
            c += indel_len + 3
        elif base_list[c-1] == "^":
            c += 2
            start_flag = True
        elif base_list[c-1] == "$":
            c += 1
            base_list_new[:-1] + [base_list_new[-1].lower()]
        elif base_list[c-1] == "*":
            c += 1
        elif base_list[c-1] == "." or base_list[c-1] == ",":
            base_list_new.append(ref.upper())
            c += 1
        else:
            if start_flag:
                base_list_new.append(base_list[c-1].lower())
            else:
                base_list_new.append(base_list[c-1].upper())
            start_flag = False
            c += 1    
    return base_list_new


def process_qual(qual_list):
    """Procesa un string de calidad. Input: ASCII string. Output:INT string"""
    qual_list_new = []
    for qual in qual_list:
        qual_list_new.append(ord(qual))
    return qual_list_new


def filter_by_qual(base_list_new, qual_list_new):
    """Elimina bases con calidad inferior a 20.
    Input: lista de bases, lista de calidades como integers.
    Output: lista de bases trimmeadas en base a su score de calidad.
    """
    c = 0
    base_list_filtered = []
    qual_list_filtered = []
    for base, qual in zip(base_list_new, qual_list_new):
        if qual >= 20:
            base_list_filtered.append(base)
            qual_list_filtered.append(qual)
    return base_list_filtered


def get_base(ref, base_list_filtered):
    """ Determina que base corresponde en una posicion dada.
    Input: base de referencia, lista de bases en esa posicion
    Output: base mas probable, conteo de esa base, prop de read tails,
    depth total, prop de base ref
    """
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
    """ Evalua la base considerando su contexto, considerando depth e indels
    Input: lista de elementos de secuencia que contienen la salida de get_base
    Output: base a imprimir
    """
    final_seq = ""
    c = 0
    while c < len(seq):
        if "-" in seq[c][0]:
            del_len = int(re.findall('\d+', seq[c][0])[0])
            isdel = is_del(seq, c, del_len)
            if isdel:
                final_seq += seq[c][0][0]
                c += del_len + 1
            else:
                final_seq += seq[c][0][0]
                c += 1
        elif "+" in seq[c][0]:
            final_seq += "".join(re.findall('[A-Z]', seq[c][0]))
            c += 1
        else:
            final_seq += seq[c][0]
            c += 1
    print ">" + name
    print final_seq


def parse_entry(entry):
    """ Parsea los registros de pileup para posterior procesado y controla
    el pipeline  Input: linea de una salida de pileup
    Output: lista de bases +info a ser evaluada por process_seq()
    """
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
    """Punto de entrada, si hay info llama a parse_entry, sino utiliza
    fasta como guia   Input: pileup file, multifasta
    Output: imprime la secuencia procesada """
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
                            seq.append((fasta_seq[count - 1], 0))
                            count += 1
                        seq.append(parse_entry(entry))
                        count += 1
        process_seq(seq, name)

if __name__ == "__main__":
    pileup_file = sys.argv[1]
    fasta_file = sys.argv[2]
    main(pileup_file, fasta_file)
