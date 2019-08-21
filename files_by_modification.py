from arcapix.fs.gpfs import ManagementPolicy, MapReduceRule

# create a management policy
p = ManagementPolicy()

# define a rule that will build a list of path names
r = p.rules.new(MapReduceRule, 'modlist', mapfn=lambda x: [x.path])

# sort by modification time
r.change(sort="current_timestamp - modification_time")

# only list path_name attribute
r.change(show=r.show_attributes('PATH_NAME'))

# include directories, links, etc in list
r.change(directories_plus=True)

# run the policy and grab the result
result = p.run('mmfs1')['modlist']

# Write the compete sorted list of files to a txt file
with open('files.txt', 'w') as f:
    for line in result:
        f.write(line + '\n')
