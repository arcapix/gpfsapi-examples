"""Example of using a Management Policy to delete files.

This example will delete '.ptc' type files, which haven't been accessed in over 90 days, owned by user 'prman'
"""

from arcapix.fs.gpfs import ManagementPolicy, DeleteRule, Criteria
from pwd import getpwnam

# create management policy
p = ManagementPolicy()

# create delete rule
r = p.rules.new(DeleteRule)

# match files with '.ptc' extension
r.criteria.new(Criteria.like('name', '*.ptc'))

# match file with not accessed in over 90 days
r.criteria.new(Criteria.gt('access', 90))

# match files owned by user 'prman'
r.criteria.new(Criteria.eq('user', getpwnam('prman').pw_uid))

# execute delete rule
p.run('mmfs1')
