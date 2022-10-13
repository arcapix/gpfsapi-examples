#!/usr/bin/env python3
"""Example tree walk using PixStor CLib.

CLib provides equivalents of some functions from the Python 'os' module

This script demonstrates walking a directory tree and writing file paths and sizes to an output file.

The 'stat' method is slower than os.stat, but potentially more accurate.
The 'lstatlite' method is roughly as fast as os.stat, and doesn't follow symlinks.

See the CLib docs for more details on lstatlite and configuring its accuracy.
"""

import os
import sys

from arcapix.fs.gpfs.clib.utils import walk
from arcapix.fs.gpfs.clib.stat import stat, lstatlite


def export_metadata(top, outfile):
    with open(outfile, 'w') as out:

        for root, dirs, files in walk(top):

            for f in files:
                path = os.path.join(root, f)
                out.write(f"{path},{lstatlite(path).st_size}\n")

            for d in dirs:
                path = os.path.join(root, d)
                out.write(f"{path},{lstatlite(path).st_size}\n")


def main():
    top = sys.argv[1]
    outfile = sys.argv[2]

    export_metadata(top, outfile)


if __name__ == '__main__':
    main()
