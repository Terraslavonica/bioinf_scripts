#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys


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
    return taxon_lib


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


if __name__ == '__main__':
    main()
