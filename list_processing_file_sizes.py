#!/usr/bin/env python3
"""Generate a file containing paths and file sizes using a ListProcessingRule.

A ListProcessingRule performs a policy scan, collecting all found files together.
The files are then passed to the specified 'processor' function to be processed sequentially.
"""
import sys

from arcapix.fs.gpfs import ManagementPolicy, ListProcessingRule


def export_metadata(files, outfile):
    """Iterate over `files` from the policy scan writing path and size to `outfile`.

    The `files` parameter is an iterator of 'file attribute' objects

    The attributes on these objects are controlled by the rule's `show` paramemter.
    If `show` isn't specified then all supported attributes,
    including everything you might expect from a 'stat' call, are included.
    The file name and path are always included.
    """
    with open(outfile, 'w') as out:
        for f in files:
            out.write(f"{f.path},{f.size}\n")


def main():
    top = sys.argv[1]
    outfile = sys.argv[2]

    policy = ManagementPolicy()

    policy.rules.new(
        ListProcessingRule,
        'list_files',

        # python function to process the found files
        processor=lambda f: export_metadata(f, outfile),

        # include directories, symlinks, etc.
        directories_plus=True,

        # we're only interested in file size
        # (path is provided for free)
        show=ListProcessingRule.show_attributes("FILE_SIZE"),
    )

    policy.run(top)


if __name__ == '__main__':
    main()
