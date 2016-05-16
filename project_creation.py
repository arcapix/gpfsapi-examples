#!/opt/arcapix/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2015 ArcaPix Limited
# All Rights Reserved.
#
#    Licensed under the ArcaPix API License, Version 1.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.arcapix.com/licenses/ArcaPix-API-1.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
'''
This is a project creator that uses a config file to create a project setup
similar to the example shown below.

If snapshotsEnabled is set to True then we need to make the initial project an 
independent fileset so that the user can snapshot the whole project.

with the Below example, 'projectRootDir' would be placed in the default pool, 
'nas-renders' in the 'NAS' pool and 'realtime-plates' in the realtime pool. 
This allows us to better manage what data is on which disks.

    mmfs1
    └── projectRootDir
        └── NewProject
            ├── nas-renders
            └── realtime-plates

The config file that was used to create the above example might look something
like the example below:

    [Commercial]
    type            = commercial
    filesystem      = mmfs1
    snapshotEnabled = True
    realtime        = plates
    nas             = renders
    inodes          = 1024
    
Instructions:

Usage: projectCreation.py [options]

Options:
  -h, --help            show this help message and exit
  -n NAME, --name=NAME  specify the project name
'''
import uuid
import ConfigParser
import sys
from optparse import OptionParser
#import the pythonAPI
from arcapix.fs.gpfs import Cluster
from arcapix.fs.gpfs.fileset import IndependentFileset
from arcapix.fs.gpfs.fileset import DependentFileset

#Create and configure the parser object to allow us to take user input
parser = OptionParser()

parser.add_option("-n",     "--name",
                  action    = "store",
                  dest      = "name",
                  default   = False,
                  help      = "specify the project name")

(options, args) = parser.parse_args()

if not options.name:
    
    print "Command Failed: You must specify a name for your project"
    sys.exit(2)

#initiate the configParser object and give it the config file
configfile        ='project_creation_template.ini'
config            = ConfigParser.ConfigParser()
config.read(configfile)

#Lets get all of our settings from the config file in one place
try:
    
    projectName     = str(options.name)
    projectRootDir  = config.get('Defaults','projectrootdir').rstrip('//')
    filesystemName  = config.get('Commercial', 'filesystem')
    inodes          = config.get('Commercial', 'inodes')
    snapshotEnabled = config.get('Commercial', 'snapshotEnabled')
    linkAddress     = projectRootDir + '/' + projectName
    #lets generate lists of the underlying filesets
    nasdeps         = config.get('Commercial', 'nas').split(',')
    realtimedeps    = config.get('Commercial', 'realtime').split(',')
except:
    
    print "Command Failed: Configuration error"
    sys.exit(1)

#Let's make sure that the given filesystem exists
#We need a cluster object to access the filesystems 
mycluster = Cluster('democluster')

if filesystemName not in mycluster.filesystems:
    
    print "Command Failed: The given filesystem in the config file could not be found"
    sys.exit(2)

'''
Now that we have all the information that we need, we need to make the head of the
project before creating it's underlying filesets. 
'''

if snapshotEnabled:
    
    #Create an independent fileset in here
    #We need a UUID for the fileset, so let's generate that
    uuidcode    = uuid.uuid4()
    #Create the Independent Fileset object
    newProject  = IndependentFileset(filesystemName, projectName, uuidcode, maxInodes=1000000, allocInodes=inodes)
    #Create the fileset in GPFS
    newProject.create()
    #Generate the link for the fileset then link it
    newProject.link(linkAddress)

else:
    
    #create a dependent fileset here
    #Generate the UUID
    uuidcode    = uuid.uuid4()
    #Create and setup the fileset object
    newProject = DependentFileset(filesystemName, projectName, uuidcode )
    #We can use 'root' inode space
    newProject._inodeSpace = 'root'
    #Create and link the fileset
    newProject.create()
    newProject.link(linkAddress)
    
'''
Now that we have set up the initial project, we need to create the underlying directories.
We will do that below by cycling through the nasdeps and realtimedeps lists that we gathered 
earlier.
'''
for fst in nasdeps:
    
    #Create nas dependent filesets
    #We want to name it with a sensible name and so that it is placed correctly
    name     = 'nas-' + projectName + '-' + fst
    #We need it to nest under the initial project so let's make it's link there
    link     = linkAddress + '/' + fst
    uuidcode = uuid.uuid4()
    #create the dependentFileset object
    newFst = DependentFileset(filesystemName, name, uuidcode )
    #As this is a dependent fileset, we need to give it an inode space.
    #If the project has snapshotEnabled, we can use that. Otherwise, 
    #we will have to use root.
    if snapshotEnabled:
        
        inodeSpace = projectName
    else:
        
        inodeSpace = 'root'
    #set the inodeSpace
    newFst._inodeSpace = inodeSpace
    #Now we can create and link the fileset in GPFS
    newFst.create()
    newFst.link(link)
            
#Lets do it all again for the realtime filesets               
for fst in realtimedeps:
    
    #create all realtime dependent filesets
    #We want to name it with a sensible name and so that it is placed correctly
    name     = 'realtime-' + projectName + '-' + fst
    #We need it to nest under the initial project so let's make it's link there
    link     = linkAddress + '/' + fst
    uuidcode = uuid.uuid4()
    #create the dependentFileset object
    newFst = DependentFileset(filesystemName, name, uuidcode )
    #As this is a dependent fileset, we need to give it an inode space.
    #If the project has snapshotEnabled, we can use that. Otherwise, 
    #we will have to use root.
    if snapshotEnabled:
        
        inodeSpace = projectName
    else:
        
        inodeSpace = 'root'
    #set the inodeSpace
    newFst._inodeSpace = inodeSpace
    #Now we can create and link the fileset in GPFS
    newFst.create()
    newFst.link(link)