#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import re
import csv
import os
from Bio.Blast import NCBIXML
from ete3 import NCBITaxa

VERSION = 0.1


def setup_args():
    parser = argparse.ArgumentParser(description='XML Blast parser, v={}'.format(VERSION))

    parser.add_argument('-in',
                        '--input',
                        action='store',
                        help='Input XML file',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        action='store',
                        help='Output directory',
                        type=str,
                        required=True)

    args = parser.parse_args()

    return args


def pull_species_name(hit_def_value):
    found_res = re.split(r'[\[.+\]]', hit_def_value)
    if len(found_res) == 0:
        return 'Nothing found'
    elif len(found_res) == 1:
        return found_res[0]
    else:
        return found_res[1]


def main():
    args = setup_args()
    print('START \n')
    if os.path.exists(args.input):
        print('Found {}'.format(args.input))
    else:
        print('Incorrect input. No .xml file in {}'.format(args.input))
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    print('Output could be found in {}'.format(args.output) + '\n')

    print('Stage I, parsing .xml file \n')
    print('Notice, stage II will require some time \n')

    handle = open(args.input)
    blast_records = NCBIXML.parse(handle)

    species_set = dict()
    try:
        while True:
            blast_record = next(blast_records)
            for i in range(len(blast_record.alignments)):
                if species_set.get(str(pull_species_name(blast_record.alignments[i].hit_def))) is None:
                    entry = 1
                else:
                    entry = species_set.get(str(pull_species_name(blast_record.alignments[i].hit_def))) + 1
                species_set.update({str(pull_species_name(blast_record.alignments[i].hit_def)): entry})
    except StopIteration:
        print('The dictionary of occurrence is built. \nCreating a .csv file ...')

    with open(args.output + '/frequency_dictionary.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['name', 'frequency_value'])
        for key, value in species_set.items():
            writer.writerow([key, value])

    print('A frequency dictionary is ready: {} \n'.format(args.output + '/frequency_dictionary.csv'))
    print('Stage II \n')

    ncbi = NCBITaxa()
    ncbi.update_taxonomy_database()

    names_list = list(species_set.keys())
    name2taxid = ncbi.get_name_translator(names_list)

    insecta_dict = {}
    mammalia_dict = {}
    bacteria_dict = {}
    archaea_dict = {}
    others_dict = {}

    for taxid in list(name2taxid.values()):
        try:
            names = ncbi.get_taxid_translator(ncbi.get_lineage(taxid[0]))
            if any("Insecta" in s for s in [names[taxid] for taxid in ncbi.get_lineage(taxid[0])]):
                insecta_dict.update(ncbi.get_taxid_translator(taxid))
            elif any("Mammalia" in s for s in [names[taxid] for taxid in ncbi.get_lineage(taxid[0])]):
                mammalia_dict.update(ncbi.get_taxid_translator(taxid))
            elif any("Bacteria" in s for s in [names[taxid] for taxid in ncbi.get_lineage(taxid[0])]):
                bacteria_dict.update(ncbi.get_taxid_translator(taxid))
            elif any("Archaea" in s for s in [names[taxid] for taxid in ncbi.get_lineage(taxid[0])]):
                archaea_dict.update(ncbi.get_taxid_translator(taxid))
            else:
                others_dict.update(ncbi.get_taxid_translator(taxid))
        except Exception:
            print('Missed taxid: {}'.format(taxid))

    dict_keeper = [insecta_dict,
                   mammalia_dict,
                   bacteria_dict,
                   archaea_dict,
                   others_dict]
    dict_names = ['/insecta_dict.csv',
                  '/mammalia_dict.csv',
                  '/bacteria_dict.csv',
                  '/archaea_dict.csv',
                  '/others_dict.csv']

    for i, elem in enumerate(dict_keeper):
        with open(args.output + dict_names[i], 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in elem.items():
                writer.writerow([key, value])

    print('Species dictionaries are compiled: {}'.format(args.output) + '\n')
    print('Parsing complete.\n')


if __name__ == '__main__':
    main()
