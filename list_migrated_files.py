#!/usr/bin/env python

import sys
from argparse import ArgumentParser

from arcapix.fs.gpfs import ManagementPolicy, ListProcessingRule, Criteria


def print_file_paths(file_list):
    for f in file_list:
        print f.pathname


def list_migrated_files(topdir):

    # Create a management policy to query the metadata
    p = ManagementPolicy()

    # Create a list rule
    r = p.rules.new(ListProcessingRule, listname='migrated_files', processor=print_file_paths)

    # Ensure files are grouped by directory
    r.change(sort='DIRECTORY_HASH')

    # Match read-managed files
    r.criteria.new(Criteria.like('MISC_ATTRIBUTES', '%V%'))

    # Run the policy
    p.run(topdir)


def main(argv=None):

    # Setup argument parser
    parser = ArgumentParser(description="list migrated files")
    parser.add_argument('path', help='the path within which to identify migrated files')

    # Process arguments
    args = parser.parse_args(argv)

    # Locate the files
    list_migrated_files(args.path)


if __name__ == "__main__":
    sys.exit(main())
