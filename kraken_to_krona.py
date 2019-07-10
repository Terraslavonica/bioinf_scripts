#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import re


def setup_args():
    parser = argparse.ArgumentParser(description='XML splitter')

    parser.add_argument('-in',
                        '--input',
                        action='store',
                        help='Input "Kraken2" file',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        action='store',
                        help='Output directory',
                        type=str,
                        required=False)

    return parser.parse_args()


def check_output_path(res_path):
    if type(res_path) is None:
        finally_path = os.getcwd() + '/results'
        if not os.path.exists(finally_path):
            os.makedirs(finally_path)
    elif not os.path.exists(res_path):
        os.makedirs(res_path)
        finally_path = res_path
        print('You can find results in {}'.format(res_path))
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


def main():
    args = setup_args()

    check_input_file(args.input, '.fastq')
    output = check_output_path(args.output)

    output_file = open(output + '/out.tsv', 'w+', 1)
    output_file.write('#queryID' + '\t' + '#taxID' + '\t' + '#score' + '\n')

    with open(args.input, 'r', 1) as file:
        for row in file:
            if re.match(rb'@SRR', row.encode('utf-8')):
                curr = re.split(r' ', row)
                query = curr[0]
                taxid = re.sub(r'[^\d]', r'', curr[-1])
                output_file.write(query + '\t' + taxid + '\t' + '1' + '\n')


if __name__ == '__main__':
    main()
