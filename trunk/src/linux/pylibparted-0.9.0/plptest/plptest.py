#!/usr/bin/env python

# plptest.py - pylibparted testing program
# Copyright (C) 2005 Ulisses Furquim <ulissesf@gmail.com>
#
# This file is part of pylibparted.
#
# pylibparted is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pylibparted is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibparted; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import sys, pylibparted

#
# test commands implementation
#

device = None
devpt = None

def device_func(args) :
    global device
    global devpt

    try :
        device = pylibparted.PedDevice(args[0])
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)

    try :
        devpt = device.diskNew()
    except pylibparted.plpError, e :
        print '>>>> Warning:', e
        devpt = None
        pass
# device_func

def mkpt_func(args) :
    global device
    global devpt

    try :
        dsktype = pylibparted.PedDiskType(args[0])
        devpt = pylibparted.PedDisk(device, dsktype)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# mkpt_func

parttype = {
    'primary'  : pylibparted.PARTITION_NORMAL,
    'extended' : pylibparted.PARTITION_EXTENDED,
    'logical'  : pylibparted.PARTITION_LOGICAL
    }

def addpart_func(args) :
    global device
    global devpt
    global parttype

    ptype = parttype[args[0]]
    start = long(args[1])
    end = long(args[2])

    try :
        anyc = device.getAnyConstraint()
        part = pylibparted.PedPartition(devpt, ptype, None, start, end)
        devpt.addPartition(part, anyc)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# addpart_func

def delpart_func(args) :
    global devpt

    try :
        part = devpt.getPartition(int(args[0]))
        devpt.delPartition(part)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# delpart_func

def resize_func(args) :
    global device
    global devpt

    num = int(args[0])
    start = long(args[1])
    end = long(args[2])

    try :
        anyc = device.getAnyConstraint()
        part = devpt.getPartition(num)
        part.setGeometry(anyc, start, end)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# resize_func

def mkfs_func(args) :
    global devpt

    num = int(args[0])
    fsname = args[1]

    try :
        part = devpt.getPartition(num)
        geom = part.getGeometry()
        fs = pylibparted.PedFileSystemType(fsname)

        geom.createFileSystem(fs)
        part.setFsType(fs)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# mkfs_func

def cpfs_func(args) :
    global device
    global devpt

    if len(args) == 3 :
        try :
            fromdev = pylibparted.PedDevice(args[0])
            fromdevpt = fromdev.diskNew()
        except pylibparted.plpError, e :
            print '>>>> Error:', e
            sys.exit(1)

        fromnum = int(args[1])
        tonum = int(args[2])
    else :
        fromdev = device
        fromdevpt = devpt
        fromnum = int(args[0])
        tonum = int(args[1])

    try :
        frompart = fromdevpt.getPartition(fromnum)
        fromgeom = frompart.getGeometry()
        fromfs = fromgeom.openFileSystem()

        topart = devpt.getPartition(tonum)
        togeom = topart.getGeometry()

        fromfs.copy(togeom)
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# cpfs_func

def resizefs_func(args) :
    global device
    global devpt

    num = int(args[0])
    start = long(args[1])
    end = long(args[2])

    try :
        part = devpt.getPartition(num)
        geom = part.getGeometry()
        fs = geom.openFileSystem()

        length = end - start + 1
        newgeom = pylibparted.PedGeometry(device, start, length)
        fs.resize(newgeom)
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# resizefs_func

def set_func(args) :
    global devpt

    num = int(args[0])
    flagname = args[1]
    value = int(args[2])

    try :
        flag = pylibparted.getPartitionFlagByName(flagname)
        part = devpt.getPartition(num)
        part.setFlag(flag, value)
        devpt.commit()
    except pylibparted.plpError, e :
        print '>>>> Error:', e
        sys.exit(1)
# set_func

#
# __main__ ;-)
#

# all possible commands a test input file can have
commands = {
    'device'   : device_func,    # device <dev>
    'mkpt'     : mkpt_func,      # mkpt <disk type>
    'addpart'  : addpart_func,   # addpart <type> <start sector> <end sector>
    'delpart'  : delpart_func,   # delpart <num>
    'resize'   : resize_func,    # resize <num> <start sector> <end sector>
    'mkfs'     : mkfs_func,      # mkfs <num> <filesystem type>
    'cpfs'     : cpfs_func,      # cpfs [from device] <from num> <to num>
    'resizefs' : resizefs_func,  # resizefs <num> <start sector> <end sector>
    'set'      : set_func        # set <num> <flag> <value>
    }

if len(sys.argv) != 2 :
    print 'Usage: %s <input file>' % sys.argv[0]
    sys.exit(1)

# Read all commands from input file
fin = open(sys.argv[1], 'r')
lines = fin.readlines()
fin.close()

# The first line should have which device we are gonna operate on :-)
ldev = lines[0]
del(lines[0])

ldev = ldev.split()
if ldev[0] != 'device' :
    print 'Error: the first line should have a device command!'
    sys.exit(1)

del(ldev[0])
print '>>> Executing command "device"'
commands['device'](ldev)

# Loop through commands and call the corresponding function handler
for line in lines :
    cmdline = line.split()

    cmd = cmdline[0]
    del(cmdline[0])

    if not cmd in commands :
        print 'Error: unknown command %s!' % cmd
        sys.exit(1)

    if cmd == 'device' :
        print 'Error: each test input file must have only one device command!'
        sys.exit(1)

    print '>>> Executing command "%s"' % cmd
    commands[cmd](cmdline)

sys.exit(0)
