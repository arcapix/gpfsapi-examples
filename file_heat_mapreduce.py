"""Example of looking up uncommon file attributes.

Arcapix list processing can look up some basic file properties by default.
For less common attributes like file heat and directory hash,
the rule's 'SHOW' expresesion must be defined explicitly in SQL format.

Once the show clause has been defined, the specified properties can be
accessed by list processing in the usual way.
"""

from __future__ import print_function
from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule

# create management policy
p = ManagementPolicy()

# create map-reduce rule
r = p.rules.new(MapReduceRule, 'heat', lambda x: [(x.path, x.fileheat)])

# define show expression to include fileheat
r.change(show="'path=' || varchar(PATH_NAME) || ' fileheat=' || varchar(FILE_HEAT)")

# execute rule and print result
print(p.run('mmfs1')['heat'])
