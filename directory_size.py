"""Lookup space usage in a directory in a GPFS filesystem (in KB)

Usage:
    python directory_size.py <path> [exclude[,exclude[,...]]]

Exclude patterns support basic wildcarding - e.g. /some/dir/*,*.txt

NB: to avoid globbing, exclude patterns should to be quoted
"""
from __future__ import print_function

import sys

from arcapix.fs.gpfs import Criteria, ListRule, ManagementPolicy


def directory_size(path, exclude=None):
    """Use policy summary parsing to find the size of a directory."""
    p = ManagementPolicy()

    if exclude:  # create exclude rule
        e = p.rules.new(ListRule, 'size', exclude=True)
        criteria = [Criteria.like('path', pattern) for pattern in exclude]
        e.criteria.new(Criteria.Or(*criteria))

    # create generic list rule
    r = p.rules.new(ListRule, 'size', directories_plus=True)

    # get summary information
    summary = p.summary(path)

    # get kb_chosen for the list rule
    return int(summary['applicability'][r.id]['kb_chosen'])


if __name__ == '__main__':
    path = sys.argv[1]

    if len(sys.argv) > 2:
        exclude = sys.argv[2].split(',')
    else:
        exclude = None

    print("%s: %d KB" % (path, directory_size(path, exclude)))
