"""Example of manipulating file xattrs.

Note - you don't need to specify 'user.<name>'
"""

from arcapix.fs.gpfs import File

f = File('/mmfs1/test.txt')

# create a new user xattr 'foo' with value 'bar'
f.xattrs.new('foo', 'bar')

# change the value of the 'foo' user xattr
f.xattrs.change('foo', 'baz')

# delete the 'foo' user xattr
f.xattrs.destroy('foo')
