"""Example of setting an xattr for all files under a directory.

Returns a list of file paths and whether the xattr was sucessfully set (TRUE/FALSE).

e.g. [('/mmfs1/somedir/test.txt', 'TRUE'), ...]
"""

from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule

# create management policy
p = ManagementPolicy()

# create map-reduce rule
r = p.rules.new(MapReduceRule, 'xattrs', lambda x: [(x.path, x.xattrset)])

# define show expression
# 'setxattr' sets the 'user.foo' xattr equal to 'bar' for all matching files and returns TRUE if successful
r.change(show="'path=' || varchar(PATH_NAME) || ' xattrset=' || varchar(setxattr('user.foo', 'bar'))")

# Only change files under 'somedir' (not including the parent directory itself)
r.criteria.new(r.criteria.like('path', '/mmfs1/somedir/*'))

# execute rule and print result
print p.run('mmfs1')['xattrs']

