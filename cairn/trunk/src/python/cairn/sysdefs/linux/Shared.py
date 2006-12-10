"""linux.Shared - Common linux code"""


import os, re
import pylibparted as parted

import cairn
from cairn import Options
from cairn.sysdefs.linux.Constants import *



##
## Shared utility functions
##


mountedFS = []


def listDevices():
	list = os.listdir("/sys/block")
	list.sort()
	cairn.debug("All devices found: %s" % " ".join(list))
	return list


def matchDevice(device, deviceRegexp = None):
	if not deviceRegexp:
		deviceRegexp = DEVICE_RE
	for pattern in deviceRegexp:
		if pattern.match(device):
			return True
	return False


def getDeviceType(device):
	if isRemovable(device):
		return None
	if matchDevice(device, LVM_RE):
		return "lvm"
	if matchDevice(device, MD_RE):
		return "md"
	if matchDevice(device, MDP_RE):
		return "mdp"
	if matchDevice(device, DRIVE_RE):
		return "drive"
	return None


def getDeviceNoPart(device):
	for regroup in ALL_DEVICE_RE:
		for regex in regroup:
			if regex.match(device):
				part = regex.sub("", device)
				return device[:-len(part)]
	return None


def getDeviceIndex(device):
	dev = getDeviceNoPart(device)
	return re.sub("[\-_a-zA-Z]+", "", dev)


def skipDevice(skips, device):
	for sdev in skips:
		if sdev == device:
			return True
	return False


def isRemovable(device):
	try:
		removable = file("/sys/block/%s/removable" % device, "r")
		line = removable.readline()
		removable.close()
		if line and line.startswith("1"):
			return True
	except:
		pass
	return False


def defineDeviceSkipped(sysdef, device, devShort, devType):
	devElem = sysdef.info.createDeviceElem(devShort)
	devElem.setChild("device", device)
	devElem.setChild("status", "skipped")
	return


def defineDevice(sysdef, device, devShort, devType):
	try:
		pdev = parted.PedDevice(device)
		devElem = sysdef.info.createDeviceElem(devShort)
		devElem.setChild("device", device)
		devElem.setChild("status", "probed")
		devElem.setChild("type", devType)
		devElem.setChild("size", "%d" % pdev.getLength())
		devElem.setChild("sector-size", "%d" % pdev.getSectorSize())
		if (devType == "drive"):
			defineDriveHW(sysdef, devElem, pdev)
		empty = False
		try:
			pdisk = pdev.diskNew()
		except Exception, err:
			if Options.get("program") == "copy":
				cairn.displayNL()
				cairn.error(str(err))
			else:
				cairn.verbose(str(err))
			devElem.setChild("status", "empty")
			empty = True
		if not empty:
			ptype = pdisk.getType()
			dlabel = sysdef.info.createDiskLabelElem(devElem)
			dlabel.setChild("type", ptype.getName())
	except Exception, err:
		cairn.displayNL()
		raise cairn.Exception("Failed to probe device:", err)
	return devElem


def defineDriveHW(sysdef, drive, pdev):
	hw = sysdef.info.createDeviceHWElem(drive)
	model = pdev.getModel()
	if model:
		hw.setChild("model", model)
	chs = pdev.getBiosCHS()
	sysdef.info.createDeviceHWGeomElem(hw, "bios-geom", "%d" % chs[0],
									   "%d" % chs[1], "%d" % chs[2])
	chs = pdev.getHwCHS()
	sysdef.info.createDeviceHWGeomElem(hw, "hw-geom", "%d" % chs[0],
									   "%d" % chs[1], "%d" % chs[2])
	return


def definePartition(sysdef, part, ppart):
	part.setChild("number", "%d" % ppart.getNum())
	geom = ppart.getGeometry()
	part.setChild("start", "%ld" % geom.getStart())
	part.setChild("size", "%ld" % geom.getLength())
	try:
		part.setChild("label", ppart.getName())
	except:
		pass
	part.setChild("type", ppart.getTypeName())
	if ppart.isActive():
		part.setChild("active", "true")
	fstype = ppart.getFsType()
	if fstype:
		part.setChild("fs-type", fstype.getName())
	flags = part.getElem("flags")
	for flag in ppart.getFlagsNames():
		flags.createElem("flag", flag)
	return


def mapPartType(type):
	if type in PART_TYPE_MAP:
		return PART_TYPE_MAP[type]
	else:
		raise cairn.Exception("Invalid partition type: %s" % type)
	return


def mount(sysdef, device, dir, opts = ""):
	cairn.log("Mounting %s on %s" % (device, dir))
	cmd = "%s %s %s %s" % (sysdef.info.get("env/tools/mount"), opts, device, dir)
	cairn.run(cmd, "Failed to mount %s on %s" % (device, dir))
	mountedFS.append(dir)
	return


def unmountAll(sysdef):
	mountedFS.reverse()
	for mount in mountedFS:
		cairn.log("Umounting %s" % mount)
		cmd = "%s %s" % (sysdef.info.get("env/tools/unmount"), mount)
		cairn.run(cmd, "Failed to unmount %s" % mount)
	return
