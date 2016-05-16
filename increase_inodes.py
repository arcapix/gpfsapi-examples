from arcapix.fs.gpfs import Cluster, IndependentFileset

threshold_pct = 80  # watermark for inode increasing
incr_pct = 20  # increase by pct
max_inode_incr = 50000  # do not increase by more than max_inode_incr

for fset in Cluster().filesystems['mmfs1'].filesets.independent().values():

    # Check if the fileset has breached its inode watermark
    if fset.allocInodes >= (fset.maxInodes * threshold_pct / 100.):

        # Increase the inodes of the fileset
        new_inodes_num = int(fset.maxInodes * incr_pct / 100.)

    # Ensure that the additional increase does not exceed the maximum inode increase
    if new_inodes_num > max_inode_incr:
        new_inodes_num = max_inode_incr

    # Add the new allocation on top of the current maximum allocation
    new_inodes_num = new_inodes_num + fset.maxInodes

    # Make the change
    fset.change(maxInodes=new_inodes_num)
