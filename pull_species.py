#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import datetime
import os
import re

import ete3
from Bio.Blast import NCBIXML

from xml_executor import core


VERSION = 0.2


def setup_args():
    parser = argparse.ArgumentParser(description='Script to pull species from .xml, version={}.'.format(VERSION))

    parser.add_argument('-i', '--input',
                        action='store',
                        help='Input .xml file',
                        type=str,
                        required=True)

    parser.add_argument('-o', '--output',
                        action='store',
                        help='The directory and the name of the output directory',
                        type=str,
                        required=False)

    parser.add_argument('--out_file',
                        action='store',
                        help='Output file',
                        type=str,
                        required=False)

    return parser.parse_args()


def pull_species_name(hit_def_value):
    found_res = re.split(r'[\[.+\]]', hit_def_value)
    if len(found_res) == 0:
        return 'Nothing found'
    elif len(found_res) == 1:
        return found_res[0]
    else:
        return found_res[1]


def name_selector(dic):
    lead_name = str()
    max_val, max_score = 100, 0
    for key in dic:
        value = dic[key]
        if value[0] == 0:
            max_score = max(max_score, value[1])
            lead_name = key
        else:
            max_val = min(max_val, value[0])
            if lead_name == '':
                lead_name = key

    return lead_name


def main():
    args = setup_args()

    print("Checking script arguments.")
    core.check_input_file(args.input, '.xml')
    output_dir = core.check_output_directory(args.output)
    output_name = core.check_output_file(args.out_file, '.csv')

    print("Connecting to database.")
    ncbi = ete3.NCBITaxa()
    if not os.path.isfile(os.getcwd() + '/ncbi_db.log'):
        logging.basicConfig(filename="ncbi_db.log", level=logging.INFO)
        logging.info("Taxonomy DB was updated {}".format(datetime.datetime.now()))
        ncbi.update_taxonomy_database()

    print("Starting the file.")
    output_file = open(output_dir + '/' + output_name, 'w+')
    output_file.write('#query_def' + '\t' + '#taxID' + '\n')
    # constant for output logging
    query_done = 0

    handle = open(args.input)
    blast_records = NCBIXML.parse(handle)

    try:
        while True:
            name_choice = dict()
            blast_record = next(blast_records)
            for i in range(len(blast_record.alignments)):
                new_name = str(pull_species_name(blast_record.alignments[i].hit_def))
                name_e_val, name_score = 100, 0
                for hsp in blast_record.alignments[i].hsps:
                    name_e_val = min(hsp.expect, name_e_val)
                    name_score = max(hsp.score, name_score)
                name_choice.update({new_name: [name_e_val, name_score]})
            selected_name = name_selector(name_choice)
            for curr_taxid in ncbi.get_name_translator([selected_name]).values():
                for j in range(len(curr_taxid)):
                    output_file.write(blast_record.query + '\t' + str(curr_taxid[j]) + '\n')
            query_done += 1
            if query_done % 1000 == 0:
                print('Done {} records.'.format(query_done))
    except StopIteration:
        print('Reading .xml is done.')

    output_file.close()


if __name__ == '__main__':
    main()
