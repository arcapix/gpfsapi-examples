from arcapix.fs.gpfs import Cluster, IndependentFileset

# Load the cluster
mycluster = Cluster()

# Delete all the test snapshots
for fset in mycluster.filesystems['mmfs1'].filesets.values():

    if isinstance(fset, IndependentFileset) and fset.name.startswith('fast-'):

        for snap in fset.snapshots.values():

            if 'test' in snap.name:

                snap.delete()
