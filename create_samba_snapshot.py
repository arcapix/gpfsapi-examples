from arcapix.fs.gpfs import Cluster
import datetime

# Load the cluster
filesys = Cluster().filesystems['mmfs1']

# Iterate the filesystems filesets
for fset in filesys.filesets.independent().values():

    # Create a snapshot name compatible with SAMBA's vss_shadow_copy2
    today = datetime.datetime.today()
    s_name = datetime.datetime.strftime(today, '@GMT-%Y.%m.%d-%H.%M.%S')

    # Create the snapshot
    fset.snapshots.new(s_name)
