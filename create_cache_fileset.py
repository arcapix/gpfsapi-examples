from arcapix.fs.gpfs import CacheFileset

# Create an AFM fileset (Using default NFS protocol and read-only cache approach)
myfileset1 = CacheFileset('mmfs1', 'cache-fileset1', '/mmfs1/projects/project1', 'gw1')

myfileset1.create()

# Change the number of read threads
myfileset1.change(afmNumReadThreads=4)

# Create another AFM fileset, using GPFS protocol
myfileset2 = CacheFileset('mmfs1', 'cache-fileset2', '/remote/mmfs1/projects/project2', protocol='gpfs')

myfileset2.create()
