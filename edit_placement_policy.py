from arcapix.fs.gpfs.policy import PlacementPolicy
from arcapix.fs.gpfs.fileset import IndependentFileset
from arcapix.fs.gpfs.rule import SetPoolRule

# create a fileset for projects
fset = IndependentFileset('mmfs1', 'projects')
fset.create()

# load placement policy for mmfs1
mypol = PlacementPolicy('mmfs1')

# get default placement rule
default = mypol.rules.defaultPlacement

# change default placement pool to 'sata1'
default.change(target='sata1')

# create placement rule for the 'projects' fileset
r = mypol.rules.new(SetPoolRule, name='proj-place', target='sas1', fileset='projects')

# save changes
# default rule will automatically be moved to end of Policy
mypol.save()