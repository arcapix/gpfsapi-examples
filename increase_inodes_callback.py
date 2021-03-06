from __future__ import print_function

import sys

from arcapix.fs.gpfs import GPFSExecuteException
from arcapix.fs.gpfs.filesystem import Filesystem
from arcapix.fs.gpfs.fileset import IndependentFileset

threshold_pct = 80  # watermark for inode increasing
incr_pct = 20  # increase by pct

soft_quota_pct = threshold_pct  # the per-fileset SoftQuota inode threshold, sensibly the same as the threshold_pct
hard_quota_pct = 95  # the per-fileset HardQuota inode threshold.
max_inode_incr = 50000  # do not increase by more than max_inode_incr


# This function will be called when the callback fires
def increase_max_inodes(fsName, filesetName):

    filesys = Filesystem(fsName)
    fset = filesys.filesets[filesetName]

    # Verify the fileset is Indepenent and has a per-fileset quota set
    if (isinstance(fset, IndependentFileset) and (fset.quotas)):

        if fset.allocInodes >= (fset.maxInodes * threshold_pct / 100.):

            new_inodes_num = int(fset.maxInodes * incr_pct / 100.)

            if new_inodes_num > max_inode_incr:
                new_inodes_num = max_inode_incr

            new_inodes_num = new_inodes_num + fset.maxInodes

            new_soft_inode_quota = int(new_inodes_num * soft_quota_pct / 100.)
            new_hard_inode_quota = int(new_inodes_num * hard_quota_pct / 100.)

            try:
                fset.change(maxInodes=new_inodes_num,
                            filesSoftLimit=new_soft_inode_quota,
                            filesHardLimit=new_hard_inode_quota)

            except GPFSExecuteException:
                pass  # alert here via your method of choice


if __name__ == '__main__':

    fsName = sys.argv[1]
    filesetName = sys.argv[2]

    filesys = Filesystem(fsName)
    fset = filesys.filesets[filesetName]

    if isinstance(fset, IndependentFileset):

        # Set an initial Quota
        soft = int(fset.maxInodes * soft_quota_pct / 100.)
        hard = int(fset.maxInodes * hard_quota_pct / 100.)

        fset.quotas.fileset.new(filesSoftLimit=soft, filesHardLimit=hard)

        # Set the Callback on the Fileset
        fset.onSoftQuotaExceeded.new(callbackId='increase_max_inodes-%s' % fset.name, command=increase_max_inodes)

    else:
        print('Auto-increases via quota triggers can only be set on Independent Filesets.')
        sys.exit(1)

    # Exit nicely
    sys.exit(0)
