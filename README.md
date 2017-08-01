# gpfsapi-examples [![Analytics](https://ga-beacon.appspot.com//UA-68292403-4/ga-beacon/readme?pixel&useReferer)](https://github.com/igrigorik/ga-beacon)

This repository contains end-user examples of the ArcaPix Python API for GPFS/Spectrum Scale.

For further documentation please see: <http://arcapix.com/gpfsapi>

If you wish to contribute an example, please submit a pull request.

## Contents
```
basic_snapdiff.py                 - Find file creations and deletions between two snapshots

change_threshold_migration.py     - Change the Placement Policy threshold migration for a given Pool

create_cache_fileset.py           - Create AFM (cache) Filesets using NFS or GPFS protocol

create_samba_snapshot.py          - Create snapshots of all Independent Filesets using 
                                    SAMBA VSS shadow_copy2 compliant names

delete_by_file_access_name.py     - Delete files matching a name not accessed in N days

delete_snapshots.py               - Delete all fast pool Independent Fileset snapshots that 
                                    have 'testarcapixexample' in their name

directory_size.py                 - Use policy summary parsing to get the size of a directory

edit_management_policy.py         - Load and modify an existing Management Policy from a .pol file

edit_placement_policy.py          - Load and modify a Filesystem's running Placement Policy

example.pol                       - An example Policy file for the 'edit_management_policy.py' script

file_heat_mapreduce.py            - Processing FILE_HEAT via MapReduceRule

files_by_modification.py          - Build a list of all files on the filesystem, sorted by modification

fileset_creation.py               - A wrapper for the mmcrfileset command that shows how to 
                                    work with Filesets in the API

find_all_xattrs.py                - List all extended attributes of the files on the filesystem

find_duplicate_files.py           - List groups of files which contain the same data

increase_inodes_callback.py       - Increasing the inodes for an Independent Fileset via 
                                    softQuotaExceeded triggering a serialised Callback

increase_inodes.py                - Increasing the inodes for an Independent Fileset via basic rules

Project_creation.py               - Creates a project consisting of a multiple Filesets within a Fileset
                                    (Independent or Dependent) utilising a config file

project_creation_templates.ini    - Config file for Project_creation.py

Readme.md                         - This file

size_histogram.py                 - Build a histogram of file sizes and print the result in tabular form
                                    If matplotlib is available, a plot can also be generated.

snapshot_creation.py              - A Snapshot creation tool that allows you to create a Snapshot of all 
                                    Independent Filesets in a Pool and sends an email notification 
                                    of Snapshots created

temp_file_size.py                 - Find the disk space used by temporary files using List Processing

type_sizes_piechart.py            - Plot a pie chart of disk space used by different file types using 
                                    List Processing and matplotlib
                         
xattr_delete_matching.py          - Delete all file with a particular xattr using a management policy

xattr_modify_file.py              - Examples of modifying a file's xattrs

xattr_set_recursive.py            - Set an xattr for all files under a directory using a policy

```
