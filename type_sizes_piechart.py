from collections import Counter
from os.path import splitext

import matplotlib.pyplot as plt

from arcapix.fs.gpfs import ListProcessingRule, ManagementPolicy


def type_sizes(file_list):
    c = Counter()

    for f in file_list:
        c.update({splitext(f.name): f.filesize})

    return c

p = ManagementPolicy()

r = p.rules.new(ListProcessingRule, 'types', type_sizes)

result = p.run('mmfs1')['types']

plt.pie(list(result.values()), labels=list(result.keys()), autopct='%1.1f%%')
plt.axis('equal')
plt.show()
