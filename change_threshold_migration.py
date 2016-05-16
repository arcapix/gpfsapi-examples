from arcapix.fs.gpfs.policy import PlacementPolicy
from arcapix.fs.gpfs.rule import MigrateRule

# load placement policy for mmfs1
mypol = PlacementPolicy('mmfs1')

# create a new migrate rule for 'sata1'
r = MigrateRule(source='sata1', threshold=(90,50))

# add rule to start of the policy
mypol.rules.insert(r, 0)

# save changes
mypol.save()