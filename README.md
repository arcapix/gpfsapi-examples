# gpfsapi-examples [![Analytics](https://ga-beacon.appspot.com//UA-68292403-4/ga-beacon/readme?pixel&useReferer)](https://github.com/igrigorik/ga-beacon)

This repository contains end-user examples of the ArcaPix Python API for GPFS/Spectrum Scale.

For further documentation please see: <http://arcapix.com/gpfsapi>

If you wish to contribute an example, please submit a pull request.

## Contents
```
basic_snapdiff.py		        - Find file creations and deletions between two snapshots
create_cache_fileset.py		    - Create AFM (cache) Filesets using NFS or GPFS protocol
create_samba_snapshot.py	    - Create snapshots of all Independent Filesets using 
									SAMBA VSS shadow_copy2 compliant names
delete_snapshots.py             - Delete all fast pool Independent Fileset snapshots that 
									have 'testarcapixexample' in their name
fileset_creation.py		        - A wrapper for the mmcrfileset command that shows how to 
									work with Filesets in the API
increase_inodes_callback.py	    - Increasing the inodes for an Independent Fileset via 
									softQuotaExceeded triggering a serialised Callback
increase_inodes.py		        - Increasing the inodes for an Independent Fileset via basic rules
Project_creation.py		        - Creates a project consisting of a multiple Filesets within a Fileset
									(Independent or Dependent) utilising a config file
project_creation_templates.ini	- Config file for Project_creation.py
Readme.md			            - This file
snapshot_creation.py		    - A Snapshot creation tool that allows you to create a Snapshot of all 
									Independent Filesets in a Pool and sends an email notification 
									of Snapshots created
temp_file_size.py		        - Find the disk space used by temporary files using List Processing
type_sizes_piechart.py		    - Plot a pie chart of disk space used by different file types using 
									List Processing and matplotlib
edit_management_policy.py       - Load and modify an existing Management Policy from a .pol file
example.pol                     - An example Policy file for the 'edit_management_policy.py' script
edit_placement_policy.py        - Load and modify a Filesystem's running Placement Policy
change_threshold_migration.py   - Change the Placement Policy threshold migration for a given Pool
```
