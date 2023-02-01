# Split the ascii input file into smaller files

import argparse
import os
import sys


# Default number of lines for output files
MAX_LINES_DEFAULT = 50


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Split input file into smaller files")
    parser.add_argument('files', nargs='+')
    parser.add_argument(
        "-p", "--preamble", action="store",
        help='Header file to prepend to each output file',
        dest='preamble')
    parser.add_argument(
        "-s", "--size", type=int, action="store",
        help='Max number of lines to include in each output file',
        dest='size')
    return parser


def main(args):
    # Read header file, if any
    preamble = []
    if args.preamble:
        try:
            with open(args.preamble) as fp:
                # Read header file as an array of strings
                preamble = fp.readlines()
        except:
            print("ERROR reading header file")

    # Max number of lines for each output file
    max_lines = MAX_LINES_DEFAULT
    if args.size:
        max_lines = args.size

    count = 0
    try:
        for input_filename in args.files:
            with open(input_filename) as fp:
                # Output file
                input_filename_parts = os.path.splitext(input_filename)
                output_filename = input_filename_parts[0] + "-" + str(int(count/max_lines)) + input_filename_parts[1]
                print("Generating {}...".format(output_filename))
                outfile = open(output_filename, 'w')

                # Add header
                print(preamble)
                outfile.writelines(preamble)

                # Iterate over each line in the file
                while True:
                    count += 1
                    line = fp.readline()

                    if not line:
                        break
                    print("  {}".format(line.strip()))
                    outfile.write(line)

                    if count % max_lines == 0:
                        # Close previous output file and start a new one
                        outfile.close()
                        output_filename = input_filename_parts[0] + "-" + str(int(count/max_lines)) + input_filename_parts[1]
                        print("-----------------------------------" + str(count))
                        print("Generating {}...".format(output_filename))
                        outfile = open(output_filename, 'w')

                        # Add header
                        print(preamble)
                        outfile.writelines(preamble)

                outfile.close()

    except Exception as ex:
        print("ERROR processing {}: {}".format(input_filename, str(ex)))


parser = init_argparse()
args = parser.parse_args()
main(args)

