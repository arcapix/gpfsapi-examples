#!/usr/bin/env python2.7
"""Identify files which contain the same data (duplicates) based on md5sum of file

Caveats:

- This method is likely to be quite slow and resource heavy

- Empty files will be listed as duplicates of each other.

- Python's 'open' method follows symlinks, so they wil be identified as duplicates

- Files that can't be read for whatever reason (e.g. permission denied) will be skipped
"""

from __future__ import print_function
import hashlib

from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule


# method to calculate md5sum of a file
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
    except:
        # exclude any files that can't be read
        return None
    return hash.hexdigest()


# build dict of format: (hash, [list, of, paths])
def reducefn(x, y):
    for k, v in y.items():
        if k is None:
            # couldn't md5sum file -> skip
            continue
        x.setdefault(k, []).extend(v)
    return x


# yield lists containing duplicates
def output(out):
    for v in out.items():
        if len(v) > 1:
            yield v

# create policy
p = ManagementPolicy()

# create MapReduceRule with relevant processing methods
r = p.rules.new(MapReduceRule, 'duplicates',
                mapfn=lambda f: {md5sum(f.path): [f.path]},
                reducefn=reducefn, output=output, initial={})

# set 'SHOW' clause to only include fields we're interested in (path)
# this can give a slight speed/efficiency boost
r.change(show=r.show_performance())

# run policy against filesystem 'mmfs1'
res = p.run('mmfs1')['duplicates']

# print formatted results
for item in res:
    print(", ".join(item), '\n')


# $ python find_duplicate_files.py
#/mmfs1/.policytmp/pdtest-b81839f8-13909.A590830A.0, /mmfs1/.policytmp/pdtest-7a781e4a-13909.A590830A.0.out
#
#/mmfs1/.policytmp/apsync.list.d70aac39.0, /mmfs1/.policytmp/apsync.list.bfeb0b4e.0
#
#/mmfs1/logs/2016/12/12/11/condor-45.err, /mmfs1/logs/2016/12/08/10/condor-42.err,
#/mmfs1/logs/2016/12/08/10/condor-43.err, /mmfs1/logs/2016/12/08/12/condor-44.err
