#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import re
from Bio import SearchIO



def setup_args():
    parser = argparse.ArgumentParser(description='XML shotener')

    parser.add_argument('-i',
                        '--input',
                        action='store',
                        help='input file',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        action='store',
                        help='Output file',
                        type=str,
                        required=False)
    
    parser.add_argument('-e',
                        '--evalue',
                        action='store',
                        help='N such that the maximum allowable evalue equels 10^{-N}',
                        type=float,
                        required=False)
    
    parser.add_argument('-b',
                        '--bitscore',
                        action='store',
                        help='Minimum allowable bit-score',
                        type=float,
                        required=False)

    return parser.parse_args()



def sort_xml(path_to_file, evalue_max, bitscore_min):
    hits = []
    blast_qresults = SearchIO.parse(path_to_file, "blast-xml")
    for blast_qresult in blast_qresults:
        for hit in blast_qresult.hits:
            if len(hit) == 1:
                hits.append(hit[0].evalue < evalue_max and hit[0].bitscore > bitscore_min)
            else:
                hits.append(min(map(lambda hit: hit.evalue, hit)) < evalue_max and max(map(lambda hit: hit.bitscore, hit)) > bitscore_min)
    return hits



def copy_file(hits, input_file, output_file = ''):
    if output_file == '':
        output_file = input_file
    with open(input_file, 'r') as file1:
        with open(output_file, 'w') as file2:
            i = 0
            row = ''
            while True:
                row = file1.readline()
                if not bool(row):
                    break
                if re.sub(r'\s+', '', row) == '<Hit>':
                    i += 1
                    if not hits[i-1]:
                        while re.sub(r'\s+', '', row) != '</Hit>':
                            row = file1.readline()
                        continue
                file2.write(row)    



def main():
    args = setup_args()
    hits = sort_xml(args.input, 10**(-args.evalue), args.bitscore)
    copy_file(hits, args.input, args.output)



if __name__ == '__main__':
    main()
