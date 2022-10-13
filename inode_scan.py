#!/usr/bin/env python3
"""Generate a list of file paths and sizes using an inode scan.

Inode scans are light-weight and fast, providing object metadata but NOT paths.
Therefore, if we need paths we have to perform a tree walk and then match inode numbers.

This is a simple example.

Inode scanning is most efficient when it is scanned in the forward direction. Scanning backwards incurs a performance penalty.
For this reason, we sort the items in each directory to reduce the number of times we scan backwards.

This approach works well for trees containing large directories, and poorly when there are lots of small directories.

For maximum efficiency, we can perform a full tree walk - holding the results in memory or writing to file,
depending on how large the directory tree is - then sort the walk results in inode number order
and perform the inode scan in complete order.

The performance for doing a complete walk and ordered scan is comparable to that of a policy scan.
"""

import os
import sys

from arcapix.fs.gpfs.clib.file import get_fileset_name
from arcapix.fs.gpfs.clib.fssnap import get_fssnaphandle_by_name
from arcapix.fs.gpfs.clib.inode import close_inodescan, open_inodescan, stat_inode
from arcapix.fs.gpfs.clib.utils import scandir, get_fsname_by_path


def scan_metadata(top, iscan):
    """Perform a tree walk using an inode scan to get file stats.

    Yields (path, iattr) pairs, where iattr contains basic file metadata
    """
    # sort the directory entries by inode number
    # this makes the inode scanning more efficient
    entries = sorted(scandir(top), key=lambda e: e.inode())

    for entry in entries:
        # scan to the specific inode, returning an 'iattr' object
        # see the CLib docs 'Inode Scanning' page
        iattr = stat_inode(iscan, entry.inode())

        yield entry.path, iattr

        # recurse to scan child directories
        if entry.is_dir():
            yield from scan_metadata(entry.path, iscan)


def main():
    top = sys.argv[1]
    outfile = sys.argv[2]

    # get the filesystem identifier and fileset name
    # for the directory being scanned
    fs = get_fsname_by_path(top)
    fd = os.open(top, os.O_RDONLY)
    fset = get_fileset_name(fd)
    os.close(fd)

    # set to None for root to do a full filesystem scan
    # otherwise we would only scan the root fileset
    # which excludes any other filesets in the filesystem.
    # (Depending on use case, this may be preferable).
    if fset == "root":
        fset = None

    fssnap = get_fssnaphandle_by_name(fs, fsetName=fset)

    iscan = open_inodescan(fssnap)
    try:
        with open(outfile, 'w') as out:

            for path, iattr in scan_metadata(top, iscan):
                out.write(f"{path},{iattr.ia_size}\n")

    finally:
        close_inodescan(iscan)


if __name__ == '__main__':
    main()
