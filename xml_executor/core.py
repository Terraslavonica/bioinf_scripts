import os
import sys


def check_input_file(input_name, extension):
    file_ext = os.path.splitext(input_name)[1]
    if file_ext == extension:
        if os.path.isfile(input_name):
            print('Found {}'.format(input_name))
        else:
            print("No {} found.".format(input_name))
            sys.exit("Exit.")
    else:
        print("Incorrect input extension. Expected {}.".format(extension))
        sys.exit("Exit.")


def check_output_directory(output):
    dir_flag = True

    if output is None:
        final_directory = os.getcwd() + '/results'
        if os.path.exists(final_directory):
            dir_flag = False
    else:
        if os.path.exists(output):
            final_directory = output
            dir_flag = False
        else:
            pre_path, pos_path = os.path.split(output)
            if pre_path == '':
                final_directory = os.getcwd() + '/' + pos_path
            else:
                final_directory = output

    if dir_flag:
        try:
            os.mkdir(final_directory)
        except OSError:
            print("Something went wrong... Please, chose another output directory.")
            sys.exit("Exit.")

    return final_directory


def check_output_file(output_name, extension):
    if output_name is None:
        final_name = '/results' + extension
        if os.path.isfile(final_name):
            print("Found {}".format(final_name))
            print("This file will be overwritten.")
    else:
        file_name, file_ext = os.path.splitext(output_name)
        if file_ext == '':
            print("Oops, you forgot to set extension or filename.")
            sys.exit("Exit.")
        else:
            if file_ext == extension:
                if os.path.isfile(output_name):
                    print("Found {}".format(output_name))
                    print("This file will be overwritten.")
                    final_name = output_name
                else:
                    print("Output file is {}".format(output_name))
                    final_name = output_name
            else:
                print("Oops, wrong extension. Expected {}.".format(extension))
                sys.exit("Exit.")

    return final_name
