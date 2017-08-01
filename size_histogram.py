#!/usr/bin/env python
"""Create a histogram of file sizes on a GPFS filesystem.

Usage:
    python size_histogram.py <target> [-o filename]

Uses Python API MapReduceRule to build the histogram
and prints the results in tabular form - e.g.

    Size      Count
    ---------------
    0B          667
    64K          47
    256K         10
    ...

Can also generate a plot image using Matplotlib (if available).
"""

from itertools import izip as zip
from argparse import ArgumentParser

from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule

try:
    import matplotlib
    # enable plot rendering without X11
    matplotlib.use('Agg')
    
    import matplotlib.pyplot as plt
    PLOT = True

except ImportError:
    PLOT = False


# bin boundaries for histogram
BOUNDS = [0, 64*1024, 256*1024, 1*1024*1024, 4*1024*1024, 100*1024*1024, 500*1024*1024, 1024*1024*1024]
LABELS = ['0B', '64K', '256K', '1M', '4M', '100M', '500M', '1G+']


def mapfn(f):
    """Return the index of the bin the file size belongs to.
    
    e.g. 50 -> 0
    """
    i = 0
    size = f.size
    while i < len(BOUNDS)-1 and size >= BOUNDS[i+1]:
        i += 1
    return i
    
def combinefn(x, inx):
    """Increment counts array for given index.
    
    e.g. [0, 0, ...], 0 -> [1, 0, ...]
    """
    x[inx] += 1
    return x

def reducefn(x, y):
    """Combine counts arrays.
    
    e.g. [12, 7, ...], [3, 1, ...] -> [15, 8, ...]
    """
    for i, v in enumerate(y):
        x[i] += v
    return x

def get_histogram(target):
    """Build a histogram of file sizes.
    
    :returns: an array of counts for each bin.
    """
    p = ManagementPolicy()
    
    # initialise counts array to 0
    initial = [0 for _ in BOUNDS]
    
    r = p.rules.new(
        MapReduceRule,
        'histogram',
        mapfn=mapfn,
        reducefn=reducefn,
        combinefn=combinefn,
        initial=initial
    )
    # only SHOW size field (only one we're interested in)
    r.change(show=r.show_performance())
    
    return p.run(target)['histogram']

    
def plot_histogram(values, filename):
    """Plot a histogram of values and save to the specified filename.
    
    Values are as returned from ``get_histogram``
    """
    # make sure output target is .png
    if not filename.endswith('.png'):
        filename += '.png'
            
    fig, ax = plt.subplots()
    
    x = range(len(values))
    
    # create a barchart of values
    ax.bar(x, values)
    
    # add labels
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS)
    
    # save plot
    plt.savefig(filename)
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('target', help="filesystem name or directory")
    parser.add_argument(
        '-o', '--output',
        help='save a histogram plot to the specified file (only if matplotlib is available)'
    )
    args = parser.parse_args()

    # build histogram data
    data = get_histogram(args.target)
    
    # print data in tabular form
    print "Size      Count\n---------------"
    for size, count in zip(LABELS, data):
        print size.ljust(4), str(count).rjust(10)
    
    # if matplotlib is available, create a plot of the histogram
    if PLOT and args.output:        
        plot_histogram(data, args.output)

