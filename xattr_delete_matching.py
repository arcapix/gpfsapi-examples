"""Example of using a Management Policy to delete all files with a particular xattr."""

from arcapix.fs.gpfs import ManagementPolicy, DeleteRule

# create management policy
p = ManagementPolicy()

# create delete rule
r = p.rules.new(DeleteRule)

# include directories
r.change(directories_plus=True)

# match file with given xattr
# if a file doesn't have the particular xattr, its value will be NULL
r.criteria.new("xattr('user.projectstate.archivedEXAMPLE') IS NOT NULL")

# execute delete rule
p.run('mmfs1')
