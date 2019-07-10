#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import mmap
import re


PREVIEW_ROWS = 19


def setup_args():
    parser = argparse.ArgumentParser(description='XML splitter')

    parser.add_argument('-in',
                        '--input',
                        action='store',
                        help='input file',
                        type=str,
                        required=True)

    parser.add_argument('-n',
                        '--number',
                        action='store',
                        help='The number of desired output files',
                        type=int,
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

    check_input_file(args.input, '.xml')
    output = check_output_path(args.output)

    with open(args.input, 'rb', 0) as file, \
            mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        total_hits = len(re.findall(br'(?i)</Iteration>', s))

    output_blocks = total_hits // args.number

    output_files = ['/{}.xml'.format(_) for _ in range(args.number)]

    written_counter = 0
    current_file = 0
    _ = 0
    record_flag = False
    with open(args.input, 'r', 1) as file:
        for row in file:
            if current_file < len(output_files) - 1:
                if written_counter == output_blocks:
                    current_file += 1
                    written_counter = 0
            if re.match(br'(?i)</Iteration>', row.encode('utf-8')):
                record_flag = False
                with open(output + output_files[current_file], 'a+b') as curr_rec:
                    curr_rec.write(row.encode('utf-8'))
                written_counter += 1
            if re.match(br'(?i)<Iteration>', row.encode('utf-8')):
                record_flag = True
            if record_flag:
                with open(output + output_files[current_file], 'a+b', 1) as curr_rec:
                    curr_rec.write(row.encode('utf-8'))


if __name__ == '__main__':
    main()
