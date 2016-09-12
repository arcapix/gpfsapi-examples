import operator
from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule

# create a policy object
p = ManagementPolicy()

# define a map function
# returns a set of any file xattr names
def mapfn(f):
    try:
        return set(f.xattrs.split())
    except AttributeError:
        return set()

# create a MapReduce rule
# reduce function combines individual sets to return unique xattr names
r = p.rules.new(MapReduceRule, 'xattrset', mapfn, operator.ior)

# change 'show' to list the file xattr names
# (these aren't returned by the policy engine by default)
r.change(show="('xattrs=' || GetXattrs('*', 'key'))")

# run the policy
print p.run('mmfs1')['xattrset']

# prints a set of unique file xattr names, e.g.
# {'gpfs.CLONE', 'user.foo', 'user.owner'}
