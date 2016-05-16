from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule


# List processing helper function
def helper(fobj):
    # used to compare files by name / path name / creation time
    return [(fobj.name, fobj.pathname.split('/', 4)[-1], fobj.creation)]

# Create rule to find and process files (can use same rule for both searches)
p = ManagementPolicy()

p.rules.new(MapReduceRule, 'snap', mapfn=helper, output=set)

# Interrogate the snapshots
# change paths to '/<fs_mount>/<snap_dir>/<snap_name>/<optional:sub_directory>'
out_old = p.run('/mmfs1/.snapshots/snap1/testdata')['snap']
out_new = p.run('/mmfs1/.snapshots/snap2/testdata')['snap']

# Diff
deleted = sorted(i[0] for i in (out_old - out_new))
created = sorted(i[0] for i in (out_new - out_old))
unchanged = sorted(i[0] for i in (out_old & out_new))

# Print results
print "Created:", ", ".join(created)
print "Deleted:", ", ".join(deleted)
print "Unchanged:", ", ".join(unchanged)
