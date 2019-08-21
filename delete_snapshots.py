from arcapix.fs.gpfs import Cluster

# Load the cluster
mycluster = Cluster()
filesys = mycluster.filesystems['mmfs1']

# Delete all the test snapshots
for fset in filesys.filesets.independent().values():
    if fset.name.startswith('fast-'):

        for snap in fset.snapshots.values():
            if 'test' in snap.name:
                snap.delete()
