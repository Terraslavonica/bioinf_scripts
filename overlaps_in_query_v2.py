#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import re
import numpy as np
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
                        required=True)

    return parser.parse_args()


class interval:
    def __init__(self, start:int, end:int, names:list):
        self.start = start
        self.end = end
        self.names = names
        
    def __repr__(self):
        return str((self.start, self.end)) + str(self.names)
    
    def add_element(self, new_start, new_end, name):
        self.names.append(name)
        self = interval(min(self.start, new_start), max(self.end, new_end), self.names)
        
    def overlap(self, start, end, name):
        if start > self.start or end < self.end:
            self.add_element(start, end, name)
            return True
        return False


def overlap_intervals(input_file, output_file):

    blast_qresults = SearchIO.parse(input_file, "blast-xml")


    with open(output_file, 'w') as file2:
        
        file2.write('#qresult.id' + '\t' + '#I.start' + '\t' + '#I.end' +
                                '\t' + '#hit.id' + '\t' + '#organism' + '\t' + '#evalue' + '\t' + '#bit-score' + '\n')


        for qresult in blast_qresults:
            ranges = np.array(())
            for hit in qresult:
                for hsp in hit:
                    if len(ranges):
                        ranges = np.vstack((ranges, np.array(hsp.query_range)))
                    else:
                        ranges = np.array(hsp.query_range).reshape((1,2))

            qresult_intervals = []

            if len(ranges):
                ranges.sort(axis=0)
                
                r0=ranges[0]
                for r in ranges:
                    if r[0] < r0[1]:
                        r0[1] = r[1]
                    elif r[0] > r0[1]:
                        qresult_intervals.append(interval(r0[0], r0[1], []))
                        r0 = r
                qresult_intervals.append(interval(r0[0], r0[1], []))

                for hit in qresult:
                    descr = hit.description
                    if len(re.split('[\[.+\]]', descr)) > 1:
                        organism = re.sub(' \([^)]+\)', '', re.sub('organism=', '', re.split('[\[.+\]]', descr)[1]))
                    else:
                        organism = re.sub('RecName: Full=', '', re.split(';', descr)[0])
                        organism = re.sub('LINE-1 ', '', organism)
                        print(organism)
                    for hsp in hit:
                        for I in qresult_intervals:
                            I.overlap(hsp.query_range[0], hsp.query_range[1], (hit.id, organism, hsp.evalue, hsp.bitscore))

                for I in qresult_intervals:
                    for name in I.names:
                        file2.write(qresult.id + '\t' + str(I.start) + '\t' + str(I.end) +
                                    '\t' + str(name[0]) + '\t' + str(name[1]) + '\t' + 
                                    str(name[2]) + '\t' + str(name[3]) + '\n')

            else:
                file2.write(qresult.id + '\t\t\t\t\t\n')





def main():
    args = setup_args()

    overlap_intervals(args.input, args.output)


if __name__ == '__main__':
    main()