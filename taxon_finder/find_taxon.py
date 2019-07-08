#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import re
import ete3
from Bio.Blast import NCBIXML


VERSION = 0.1


# TODO: нужно добавить ввод парных ридов
def setup_args():
    parser = argparse.ArgumentParser(description='Taxon finder. v={}'.format(VERSION))

    parser.add_argument('--input_taxon',
                        action='store',
                        help='File with interested taxons',
                        type=str,
                        required=True)

    parser.add_argument('--input_xml',
                        action='store',
                        help='An .xml file with blust results',
                        type=str,
                        required=True)

    parser.add_argument('--input_reads',
                        action='store',
                        help='An .fastq file with reads',
                        type=str,
                        required=True)

    parser.add_argument('--output',
                        action='store',
                        help='Directory for output',
                        type=str,
                        required=False)

    return parser.parse_args()


# TODO: изменить функцию таким образом, чтобы создавала несуществующую директорию
def check_output_path(res_path):
    if (res_path is None) or (not os.path.exists(res_path)):
        finally_path = os.getcwd() + '/results'
        if not os.path.exists(finally_path):
            os.makedirs(finally_path)
        print('You can find results in {} .'.format(os.getcwd() + '/results'))
        return finally_path
    else:
        print('You can find results in {}'.format(res_path))
        return res_path


def check_input_file(file_path, extension):
    """
    Checks if the file exists and the extension is correct.
    :param file_path: the path received from input commands to the input file.
    :param extension: the expected extension of the file.
    """
    if (os.path.isfile(file_path)) and (os.path.splitext(file_path)[1] == extension):
        print('Found {}'.format(file_path))
    else:
        print('Incorrect input. {} does not exist or was used file with inappropriate extension.'.format(file_path))
        sys.exit('Input error. Exit.')


# TODO: добавить нормальное считывание файла, нормально грепать только слова, без символов
def read_taxons(taxon_path):
    """
    Reads names of taxons line by line from file.
    :param taxon_path: the path received from input commands to the file with taxons.
    :return: set with taxon names. Set is used to avoid double entry.
    """
    handle = open(taxon_path, 'r', encoding='utf-8')
    taxon_lib = set()
    line = handle.readline()
    while line:
        taxon_lib.add(line[:-1].lower())
        line = handle.readline()
    handle.close()
    taxon_lib.discard('')
    return list(taxon_lib)


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

    print('Start')
    print('Checking commands:')

    # Here we check the input and the output,
    # in other words, we check the correction of the commands
    # TODO: сделать нормальную проверку, так как здесть она зависит от порядка ввода, а вообще-то не должна зависеть!
    for elem in zip([args.input_taxon, args.input_xml, args.input_reads],
                    ['.txt', '.xml', '.fastq']):
        check_input_file(elem[0], elem[1])
    output = check_output_path(args.output)

    # We need to get a set with names
    handle = open(args.input_xml)
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

    with open(output + '/frequency_dictionary.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['name', 'frequency_value'])
        for key, value in species_set.items():
            writer.writerow([key, value])

    # This stage requires time, because script should download database from NCBI and parse it.
    print('This stage requires additional time...')
    ncbi = ete3.NCBITaxa()
    # TODO: решить вопрос с обновлением БД
    # ncbi.update_taxonomy_database()

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
        with open(output + dict_names[i], 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in elem.items():
                writer.writerow([key, value])

    # Now we create one dict with unique keys, so that we can search easier
    overall_dict = dict()
    for d in dict_keeper:
        overall_dict.update(d)

    handle = open(args.input_xml)
    blast_records = NCBIXML.parse(handle)

    species_query_set = dict()
    try:
        while True:
            blast_record = next(blast_records)
            for i in range(len(blast_record.alignments)):
                new_name = str(pull_species_name(blast_record.alignments[i].hit_def))
                for curr_taxid in ncbi.get_name_translator([new_name]).values():
                    for j in range(len(curr_taxid)):
                        species_query_set.update({curr_taxid[j]: blast_record.query})
    except StopIteration:
        pass

    # TODO: учесть вариант нескольких значений taxon_id для файла
    # This will allow us to get a dict with taxon_id's from our input file
    taxon_dict = ncbi.get_name_translator(read_taxons(args.input_taxon))

    print('Search is started...')
    for idx, key in enumerate(taxon_dict):
        tree = ncbi.get_descendant_taxa(key, collapse_subspecies=True, return_tree=True)
        if type(tree) == list:
            if overall_dict.get(taxon_dict[key][0]) is not None:
                print('{0}:{1} is in your results'.format(key, overall_dict.get(taxon_dict[key][0])))
                print('\t{0} is at the {1}'.format(key, species_query_set.get(taxon_dict[key][0])))
        elif type(tree) == ete3.phylo.phylotree.PhyloNode:
            for child in tree.children:
                # We need only the taxid number
                potential_ids = re.findall('\\b\\d+\\b', child.get_ascii())
                for potential_id in potential_ids:
                    if overall_dict.get(int(potential_id)) is not None:
                        print('{0}:{1} is in your results'.format(key, overall_dict[int(potential_id)]))
                        print('\t{0} is at the {1}'.format(key, species_query_set[int(potential_id)]))
        else:
            print('{0}: {1} is unknown'.format(key, taxon_dict[key]))
    print('Search is finished.')


if __name__ == '__main__':
    main()
