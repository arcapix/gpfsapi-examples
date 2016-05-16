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
Instructions:

Use this script to create a dependent fileset with given parameters. All options are required.

Usage: filesetCreation [options]

Options:
  -h, --help                                show this help message and exit
  -f FILESYSTEM,  --filesystem=FILESYSTEM   Used to specify the filesystem that the project should be created on - required
  -p POOL,        --pool=POOL               Used to specify the pool for the project - required
  -n NAME,        --name=NAME               Used to specify the name of the project - required
  -d PATH,        --path=PATH               Used to specify the path for the project - required
  -m MAXINODES,   --maxInodes=MAXINODES     Used to specify the maximum number of inodes for the project - required
  -a PREALLOCATE, --preallocate=PREALLOCATE Used to specify the number of inodes to preallocate to the project - required

Example:
    projectCreate -f mmfs1 -p nas -n testerScript -d /mmfs1/data -m 2024 -a 1024
'''
from optparse import OptionParser
import re
#Imports for Arcapix API use
from arcapix.fs.gpfs import IndependentFileset
import uuid

#Create and configure the parser object to allow us to take user input for the fileset options
parser = OptionParser()

parser.add_option("-f", "--filesystem",
                  action="store",
                  dest="filesystem",
                  default=False,
                  help="Used to specify the filesystem that the project should be created on - required")
parser.add_option("-p", "--pool",
                  action="store",
                  dest="pool",
                  default=False,
                  help="Used to specify the pool for the project - required")
parser.add_option("-n", "--name",
                  action="store",
                  dest="name",
                  default=False,
                  help="Used to specify the name of the project - required")
parser.add_option("-d", "--path",
                  action="store",
                  dest="path",
                  default=False,
                  help="Used to specify the path for the project - required")
parser.add_option("-m", "--maxInodes",
                  action="store",
                  dest="maxInodes",
                  default=False,
                  help="Used to specify the maximum number of inodes for the project - required")
parser.add_option("-a", "--preallocate",
                  action="store",
                  dest="preallocate",
                  default=False,
                  help="Used to specify the number of inodes to preallocate to the project - required")

(options, args) = parser.parse_args()

#Check all the options have been specified and exit if any have not
if not options.filesystem:
    print "Command failed: filesyetem must be specified to continue"
    exit()
elif not options.pool:
    print "Command failed: pool must be specified to continue"
    exit()
elif not options.name:
    print "Command failed: name must be specified to continue"
    exit()
elif not options.path:
    print "Command failed: path must be specified to continue"
    exit()
elif not options.maxInodes:
    print "Command failed: maxInodes must be specified to continue"
    exit()
elif not options.preallocate:
    print "Command failed: preallocate must be specified to continue"
    exit()

#Now we know that all the options exist
#let's get the inode user input into a  variable and ensure they are the correct type - error and exit if not
try:
    maxInodesOpts = int(options.maxInodes)
except:
    print "Command failed: maxInodes is of incorrect type"
    exit()
try:
    preallocatedOpts = int(options.preallocate)
    if preallocatedOpts > maxInodesOpts:
        print "command Failed: You can not preallocate more inodes than the maximum allocation"
        exit()
except:
    print "Command failed: preallocated is of incorrect type"
    exit()

'''
lets do the API magic from here onwards, we will create the fileset object
then create that on the GPFS filesystem. we can then link that fileset using
the given path.
'''

#We need to make an ID for the fileset 
uid = uuid.uuid4()


filesystem = options.filesystem

#The filesetName needs to be called pool-projectName for GPFS policy to then place the file in the right pool
filesetName = options.pool + '-' + options.name

#remove any trailing / from the user input (if any) then add the link to the fileset name to the path
linkAddress = re.sub("^/|/$", "", options.path) + '/' + options.name

#Create the fileset object using the user defined options
myfileset = IndependentFileset(filesystem, filesetName, uid, maxInodes=maxInodesOpts, allocInodes=preallocatedOpts)
#Create the fileset on GPFS
myfileset.create()
#link the fileset
myfileset.link(linkAddress)







