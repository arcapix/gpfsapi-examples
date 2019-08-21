from arcapix.fs.gpfs import CacheFileset

# Create an AFM fileset (Using default NFS protocol and read-only cache approach)
afm_fileset = CacheFileset('mmfs1', 'cache-fileset1', '/mmfs1/projects/project1', 'gw1')

afm_fileset.create()

# Change the number of read threads
afm_fileset.change(afmNumReadThreads=4)

# Create another AFM fileset, using GPFS protocol
gpfs_fileset = CacheFileset('mmfs1', 'cache-fileset2', '/remote/mmfs1/projects/project2', protocol='gpfs')

gpfs_fileset.create()
