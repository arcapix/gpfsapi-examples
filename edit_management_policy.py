from arcapix.fs.gpfs import ManagementPolicy
from arcapix.fs.gpfs.rule import ExcludeRule
from arcapix.fs.gpfs.criteria import Criteria

mypol = ManagementPolicy('example.pol')

# get delete rule
d = mypol.rules['del-tmp']

# set to only delete from fast pool
d.change(source='sas1')

# create a rule to exclude files in backup folders
r = ExcludeRule(name='excl-bak')
r.criteria.new(Criteria.like('path', '*backup*'))

# add new rule before delete rule
mypol.rules.insert(r, 1)

# save the resulting policy
mypol.save()
