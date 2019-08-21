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
This script is a snapshot creation tool that allows you to create a snapshot of all independent
filesets in one pool and then we will send an email listing all filesets that have had a snapshot.
This means we could run this as a cron job and be alerted of what snapshots have been created

Instructions

Used to create snapshots of:

All Filesets in a Pool

    Use the -p (--pool) option to specify a pool and the script will create a snapshot of each
    fileset within that pool

A Fileset

    Specify a fileset using the -f (--fileset) option and a name for the snapshot (-n, --name)

Global Snapshots

    If you specify neither fileset (-f --fileset) or pool (-p --pool) the script will create a
    global snapshot using the given name (-n --name)



Usage: snapshotCreation.py [options]

Options:
  -h,          --help               how this help message and exit
  -n NAME,     --name=NAME          specify the name of the snapshot to create (not required in conjunction witth -p --pool)
  -p POOL,     --pool=POOL          if you specify a pool, a snapshot of all filesets in the pool will be created
  -f FILESET,  --fileset=FILESET    specify the name of a fileset

Examples:

snapshotCreation.py -p sas1

snapshotCreation.pt -n
'''
from __future__ import print_function

import datetime
import smtplib
from optparse import OptionParser

# Imports for Arcapix API use
from arcapix.fs.gpfs import Cluster

# The name of the filesystem that we want to work with
filesystemName = 'mmfs1'

# Create and configure the parser object to allow us to take user input
parser = OptionParser()

parser.add_option("-n", "--name",
                  action="store",
                  dest="name",
                  default=False,
                  help="specify the name of the snapshot to create (not required in conjunction witth -p --pool)")
parser.add_option("-p", "--pool",
                  action="store",
                  dest="pool",
                  default=False,
                  help="if you specify a pool, a snapshot of all filesets in the pool will be created")
parser.add_option("-f", "--fileset",
                  action="store",
                  dest="fileset",
                  default=False,
                  help="specify the name of a fileset")


(options, args) = parser.parse_args()

# Email Info setup
sender = 'root@apstore.foo.bar'
receivers = ['example@example.com']

# Lets initiate a cluster and a filesystem object
mycluster = Cluster('democluster')
filesys = mycluster.filesystems[filesystemName]


if not options.name and not options.pool:

    print("Command Failed: You must specify the name for the new snapshot")
    exit()

if options.pool and options.fileset:

    print("Command Failed: You can only specify a pool OR a fileset")
    exit()


if options.filset:

    '''
    We need to make a snapshot of an individual fileset here
    '''
    # Lets check if the fileset exists first
    try:
        # We can try and pull it's data and if that fails we assume it doesn't exist
        fset = filesys.filesets.__getitem__(options.fileset)
    except:
        # Fileset is not in the Filesets object so we can not create a snapshot
        print("Command Failed: The given fileset does not exist")
        exit()
    # If we got this far then the fileset exists - let's create it's snapshot
    fset.snapshots.new(options.name)

elif options.pool:

    '''
    If we are given a pool then we need to cycle through each fileset and create
    a snapshot of it if it is in the given pool
    '''
    # Lets make a boolean so to see if any matches are found
    foundOne = False
    # Cycle through all filesets
    # Initiate a list for the email notification
    filesetList = []
    for fileset in filesys.filesets.values():

        if fileset.name.startswith(options.pool):

            foundOne = True
            # Generate the snapshot name
            today = datetime.datetime.today()
            snapshot_name = datetime.datetime.strftime(today, "@GMT-%Y.%m.%d-%H.%M.%S")
            # Create a snapshot of the fileset - we do this via the snapshot object
            fileset.snapshots.new(snapshot_name)

            # Add the fileset to the filesets list for the email notification
            filesetList.append(fileset.name)

    # If we found none - error and exit
    if foundOne == False:

        print("Command Failed: No filesets matched the search for that pool")
        exit()
    else:

        # if we get here, a snapshot was created of at least one fileset - so let's send the mail
        # We set up the sender and receiver earlier so let's generate the message here
        message = "Snapshots completed: \n" + '\n'.join(filesetList)
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)

else:

    '''
    If we are not given a pool or fileset name, we will create a global snapshot.
    '''
    # We create a gloval snapshot via the filesystem object
    filesys.snapshots.new(options.name)
