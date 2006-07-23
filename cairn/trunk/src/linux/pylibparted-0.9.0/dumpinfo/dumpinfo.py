#!/usr/bin/env python

# dumpinfo.py - example code using pylibparted to dump partition table info
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

import pylibparted

devs = pylibparted.probeAllDevices()

for p in devs :
    # Device
    d = pylibparted.PedDevice(p)
    print 'Device:', d.getPath()
    print 'Size:', d.getLength()
    
    c,h,s = d.getBiosCHS()
    chs = str(c) + '/' + str(h) + '/' + str(s)
    print 'BIOS CHS:', chs

    c,h,s = d.getHwCHS()
    chs = str(c) + '/' + str(h) + '/' + str(s)
    print 'HW CHS:', chs

    # Partition table
    pt = d.diskNew()
    parts = pt.getPartitions()

    for part in parts :
        if part.isActive() :
            print ' Partition:', part.getPath()
	    print ' Type Name:', part.getTypeName()
	    print ' ID:', part.getId()

            geom = part.getGeometry()

            print '  Start:', geom.getStart()
            print '  End:', geom.getEnd()
            print '  Length:', geom.getLength()

            fs = part.getFsType()
            if fs :
                print '  FS:', fs.getName()
    # parts
# devs
