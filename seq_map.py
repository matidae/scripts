#!/usr/bin/env python
import sys
import re
import os.path as path
from Bio import SeqIO


def process_nuc(ref, base_list):
    """Parsea una entrada de mapeo del pileup a un formato mas legible.
    Input: base de referencia, lista de bases mapeadas en formato CIGAR.
    Output: lista de bases para cada posicion
    """
    base_list_new = []
    base_list = base_list.replace(".", ref).replace(",", ref).replace("*","").upper()
    indels =  set(re.findall("\d+", base_list))
    indels = "|".join([".."+i+".{"+i+"}" for i in indels])
    base_list = re.sub('\^.(.)', lambda x:x.expand(r'\1').lower(), base_list)
    base_list = re.sub('(.)\$', lambda x:x.expand(r'\1').lower(), base_list)
    indels_new = map(lambda x:x.upper(), re.findall(indels,base_list))
    base_list = list(re.sub(indels,'',base_list))
    return base_list + indels_new


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
    base_set = list(set([x.upper() for x in base_list_filtered]))
    base_count = []
    for base in base_set:
        base_count.append(base_list_filtered.count(base))
    if sum(base_count) > 0:
        seq = base_set[base_count.index(max(base_count))]
        max_count = max(base_count)
        prop_end = base_list_filtered.count(seq.lower())*1.0/max_count
        prop_ref = (base_list_filtered.count(ref) + base_list_filtered.
                    count(ref.lower())) * 1.0 / len(base_list_filtered)
        return (seq, max_count, prop_end, len(base_list_filtered),
                prop_ref, ref)
    else:
        return (ref, 0, 0, 0, 1, ref)


def is_del(seq, c, del_len):
    """ Evalua si existe la delecion contando cuantos reads en posiciones
    posteriores avalan la delecion.
    Input: entrada con la delecion, posicion, largo de la delecion
    Output: booleano resultado de la evaluacion
    """
    for_del = seq[c][1]
    not_del = 0
    for i in xrange(del_len):
        if len(seq) > c+i+1:
            not_del += seq[c+i+1][1] * seq[c+i+1][2]
    return for_del > not_del


def process_seq(seq, fasta_seq):
    """ Evalua la base considerando su contexto, considerando depth e indels
    Input: lista de elementos de secuencia que contienen la salida de get_base
    Output: base a imprimir
    """
    final_seq = ""
    c = 0
    coord_vector = []
    while c < len(seq):
        if seq[c][4] > 0.25 and seq[c][3] > 100:
            final_seq += seq[c][5]
            coord_vector.append(0)
            c += 1
        else:
            if "-" in seq[c][0]:
                del_len = int(re.findall('\d+', seq[c][0])[0])
                isdel = is_del(seq, c, del_len)
                if isdel:
                    final_seq += seq[c][0][0]
                    coord_vector = coord_vector + [-1] * del_len
                    c += del_len + 1
                else:
                    final_seq += seq[c][0][0]
                    coord_vector.append(0)
                    c += 1
            elif "+" in seq[c][0]:
                final_seq += "".join(re.findall('[A-Z]', seq[c][0]))
                coord_vector.append("".join(re.findall('\d+', seq[c][0])))
                c += 1
            else:
                final_seq += seq[c][0]
                coord_vector.append(0)
                c += 1
    return (final_seq, coord_vector)


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
        return (ref, 0, 0, 0, 1, ref)


def write_file(name, seq, coord_vector, out_fasta, out_coord):
    out_fasta = open(out_fasta, "a")
    out_fasta.write(">" + name + "\n" + seq + "\n")
    out_fasta.close()

    out_coord = open(out_coord, "a")
    out_coord.write(name + "\t" + ",".join(map(str, coord_vector)) + "\n")
    out_coord.close()


def check_new_files(fasta_file):
    out_fasta = ""
    out_coord = ""
    if "." in fasta_file:
        out_fasta = ".".join(fasta_file.split('.')[:-1]) + ".new.fa"
        out_coord = ".".join(fasta_file.split('.')[:-1]) + ".new.coor"
    else:
        out_fasta = fasta_file + ".new.fa"
        out_coord = fasta_file + ".new.coord"
    open(out_fasta, 'w').close()
    open(out_coord, 'w').close()
    return [out_fasta, out_coord]


def compare_position(count, seq, entry, fasta_seq):
    pos = int(entry.split()[1])
    if count == pos:
        seq.append(parse_entry(entry))
        count += 1
    else:
        while count < pos:
            seq.append((fasta_seq[count-1], 0, 0, 0, 1,
                        fasta_seq[count-1]))
            count += 1
        seq.append(parse_entry(entry))
        count += 1
    return [seq, count]


def main(pileup_file, fasta_file):
    """Punto de entrada, si hay info llama a parse_entry, sino utiliza
    fasta como guia   Input: pileup file, multifasta
    Output: imprime la secuencia procesada """
    fasta = SeqIO.index(fasta_file, "fasta")
    seq = []
    count = 1
    fasta_name = ""
    out_file = check_new_files(fasta_file)
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
