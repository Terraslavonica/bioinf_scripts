#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re


def setup_args():
    parser = argparse.ArgumentParser(description='Puller from BOLD fasta file')

    parser.add_argument('-in',
                        '--input',
                        action='store',
                        help='Input file',
                        type=str,
                        required=True)

    return parser.parse_args()


def find_gaps_stat(row):
    return (len(re.findall('-', row))) / len(row)


def write_fasta(names_dict, filename):
    with open('results_{}'.format(filename), 'w+') as file:
        for name in names_dict:
            file.write('{0}|{1}\n'.format(names_dict[name][0], names_dict[name][2]))
            file.write(names_dict[name][1] + '\n')


def main():
    filename = setup_args().input
    names_dict = dict()

    with open(filename, 'r+') as file:
        for row in file:
            if row[0] == '>':
                # находим текущее название
                row_name = re.split(r'\|', row)[1]
                full_name = row[:-1]
                # проверяем, есть ли уже последовательность для этого имени
                old_seq = names_dict.get(row_name)
                if old_seq:
                    # если да, то сравниваем длины
                    curr_seq = next(file)[:-1]
                    if len(old_seq) < len(curr_seq):
                        # если новая посл-ть длиннее, то записываем
                        names_dict.update({row_name: [full_name, curr_seq, find_gaps_stat(curr_seq)]})
                else:
                    # если нет, то записываем новую посл-ть
                    curr_seq = next(file)[:-1]
                    names_dict.update({row_name: [full_name, curr_seq, find_gaps_stat(curr_seq)]})

    write_fasta(names_dict, filename=filename)


if __name__ == '__main__':
    main()
