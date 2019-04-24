#!/usr/bin/env python2.7

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

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

    # Show the full path of matched files
    r.criteria.new(Criteria.like('MISC_ATTRIBUTES', '%V%'))

    # Run the policy
    p.run(topdir)

### main

def main(argv=None):

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = "list migrated files"
    program_desc = '%s\n\nUSAGE' % (program_shortdesc)

    # Setup argument parser
    parser = ArgumentParser(
        description=program_desc,
        formatter_class=RawDescriptionHelpFormatter)
    
    parser.add_argument(
        'path', nargs=1,
        help='the path within which to identify migrated files')

    # Process arguments
    args = parser.parse_args()

    # Locate the files
    list_migrated_files(args.path[0])    

    return 0

if __name__ == "__main__":
    sys.exit(main())


# EOF

