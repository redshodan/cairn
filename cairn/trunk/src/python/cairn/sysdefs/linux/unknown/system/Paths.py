"""linux.unknown.system.Paths Module"""


import os
import stat


import cairn
from cairn import Options
from cairn import sysdefs
import cairn.sysdefs.templates.unix.system.Paths as tmpl
from cairn.sysdefs.Tools import Tool, ToolGroup
from cairn.sysdefs.linux import Constants



def getClass():
	return Paths()



class Paths(tmpl.Paths):

	def __init__(self):
		self.__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
		self.__BINS = [ Tool("mount", "env/tools/mount", True),
						Tool("umount", "env/tools/unmount", True),
						Tool("mdadm", "env/tools/mdadm", False),
						ToolGroup("env/archive-tool", "env/archive-tool-user",
								  "archive", True,
								  [ Tool("tar", "env/tools/tar", False),
									Tool("star", "env/tools/star", False) ]),
						ToolGroup("env/zip-tool", "env/zip-tool-user", "zip",
								  True,
								  [ Tool("bzip2", "env/tools/bzip2", False),
									Tool("gzip", "env/tools/gzip", False),
									Tool("compress", "env/tools/compress",
										 False) ])
						]
		for tool in Constants.LVM_COPY_TOOLS:
			self.__BINS.append(Tool(tool, "env/tools/" + tool, False))
		return


	def userCheck(self, sysdef):
		self.checkMD(sysdef)
		self.checkLVM(sysdef)
		return


	def checkMD(self, sysdef):
		if Options.get("no-raid"):
			return
		# Check for mdadm tool
		if not sysdef.info.get("env/tools/mdadm"):
			cairn.warn("Failed to find program mdadm. Software RAIDs will " +
					   "not be handled.")
			sysdef.info.setChild("env/tools/md", "False")
		cairn.debug("mdadm found")
		# Check for md module if we are copy. Restore should take care of the
		# module itself.
		if Options.get("command") == "copy":
			fail = True
			try:
				try:
					try:
						info = os.lstat("/proc/mdstat")
					except:
						raise Exception("No Software Raid kernel modules found")
					if stat.S_ISREG(info[stat.ST_MODE]):
						mdstat = file("/proc/mdstat", "r")
						for line in mdstat.readlines():
							if line.startswith("Personalities :"):
								cairn.debug("Found: %s" % line)
								arr = line.split(":")
								if (len(arr) == 2):
									raids = arr[1].strip()
									if len(raids):
										fail = False
										break
								break
					if fail:
						raise Exception("No Software Raid kernel modules found")
				finally:
					try: mdstat.close()
					except: pass
			except Exception, err:
				cairn.warn("Software Raid will not be handled: %s" % str(err))
				return
		sysdef.info.setChild("env/tools/md", "True")
		return


	def checkLVM(self, sysdef):
		if Options.get("no-lvm"):
			return
		# Check for lvm tools
		for tool in Constants.LVM_COPY_TOOLS:
			if not sysdef.info.get("env/tools/" + tool):
				cairn.warn(("Failed to find program %s. " +
							"LVM volumes will not be handled") % tool)
				sysdef.info.setChild("env/tools/lvm", "False")
				return
		cairn.debug("lvm tools found")
		# Check for LVM module if we are copy. Restore should take care of the
		# module itself.
		if Options.get("command") == "copy":
			try:
				misc = file("/proc/misc", "r")
				contents = misc.read()
				misc.close()
				if (contents.find("device-mapper") < 0):
					raise Exception("LVM kernel module (dm_mod) is not loaded")
			except Exception, err:
				cairn.warn("LVM volumes will not be handled: %s" % str(err))
				return
		# Passed everything
		sysdef.info.setChild("env/tools/lvm", "True")
		return
