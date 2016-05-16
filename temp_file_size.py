from arcapix.fs.gpfs import ManagementPolicy, ListProcessingRule, Criteria

# Create a Management Policy
p = ManagementPolicy()

# Create a ListProcessing Rule
r = p.rules.new(ListProcessingRule, listname='temp_files_bytes', processor=lambda lst: sum(x.filesize for x in lst))

# Add criteria to specify filetype
r.criteria.new(Criteria.like('name', '*.tmp'))

# Run policy
print p.run('mmfs1')

# {'tmp_files_bytes': 208456737}
