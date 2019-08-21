#!/usr/bin/env python
"""This example gets the size of a fileset from the a policy summary.

Summary works by running a policy in test mode, and parsing the policy engine preamble.

The summary includes rule 'applicability' information,
how many files, how much data (KB) a rule will select.
So by constructing a LIST rule, which matches files in a particular fileset,
we can get the total size of that fileset.

This is much faster than running a full policy scan.
"""

from __future__ import print_function

from arcapix.fs.gpfs.policy import ManagementPolicy
from arcapix.fs.gpfs.rule import ListRule


def fileset_size(filesystem, fileset, nodes='all'):

    policy = ManagementPolicy()

    # create generic list rule
    rule = policy.rules.new(ListRule, 'fileset_size')

    # match all files and directories in the given fileset
    rule.change(fileset=fileset, directories_plus=True)

    # get summary info
    summary = policy.summary(filesystem, nodes=nodes, qos='maintenance')

    # return kb_chosen for the list rule
    # NOTE - all value in 'summary' are strings
    return int(summary['applicability'][rule.id]['kb_chosen'])


if __name__ == '__main__':

    print(fileset_size('mmfs1', 'myfileset'), 'KB')
