from __future__ import absolute_import
from __future__ import print_function

import argparse

from .extractors import ExtractorFactory


def extract(filename, destination='.'):
    """
    Attempts to extract the given archive to the given destination
    """
    extractor = ExtractorFactory.create(filename, destination)
    return extractor.extract()


def parse_arguments():
    """
    Create a custom command line parser and return the arguments
    """
    parser = argparse.ArgumentParser(description="Easily extract anything")
    parser.add_argument('filename', help='File to extract')
    parser.add_argument('destination', nargs='?', default='.',
                        help='Where to put the extracted files')
    return parser.parse_args()


def main():
    """
    Parses command line aruments and extracts a given archive accordingly
    """
    args = parse_arguments()
    destination = extract(args.filename, args.destination)
    print('Contents extracted to {}'.format(destination))

if __name__ == '__main__':
    main()
