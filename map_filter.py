#!/usr/bin/env python
import sys


class Read(object):
    def __init__(self, name):
        self.name = name
        self.mapping = []


class Mapping(object):
    def __init__(self, line):
        self.line = line
        self.transitions = 0
        self.transversions = 0
        self.insertions = 0
        self.deletions = 0
        self.read_quality = 0
        self.mate_distance = 0


def main(mapping_file):
    name_aux = ""
    first = True
    with open(mapping_file) as mf:
        for line in mf:
            name = line.split()[0]
            if first:
                name_aux = name
                first = False
            elif name == name_aux:
                print 1, name
            else:
                print name
                name_aux = name
        print name


if __name__ == "__main__":
    mapping_file = sys.argv[1]
    main(mapping_file)
