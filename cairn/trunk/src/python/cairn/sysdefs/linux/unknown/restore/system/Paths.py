"""linux.unknown.restore.system.Paths Module"""


import cairn.sysdefs.linux.unknown.system.Paths as tmpl
from cairn.sysdefs.Tools import Tool, ToolGroup



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		super(Paths, self).__init__()
		bins = [ Tool("mkfs.ext2", "env/tools/mkfs.ext2", False),
				 Tool("mkfs.ext3", "env/tools/mkfs.ext3", False),
				 Tool("mkfs.xfs", "env/tools/mkfs.xfs", False),
				 Tool("mkfs.jfs", "env/tools/mkfs.jfs", False),
				 Tool("mkfs.reiserfs", "env/tools/mkfs.reiserfs", False),
				 Tool("mkswap", "env/tools/mkswap", False),
				 Tool("chroot", "env/tools/chroot", True),
				 Tool("sync", "env/tools/sync", False)
			   ]
		self.__BINS = self.__BINS + bins
		for tool in Constants.LVM_RESTORE_TOOLS:
			self.__BINS.append(Tool(tool, "env/tools/" + tool, False))
		return


	def userCheck(self, sysdef):
		self.checkMD(sysdef)
		self.checkLVM(sysdef)
		return


	def checkMD(self, sysdef):
		if Options.get("no-raid"):
			return
		return


	def checkLVM(self, sysdef):
		if Options.get("no-lvm"):
			return
		# Check for 
		for tool in Constants.LVM_COPY_TOOLS:
			if not sysdef.info.get("env/tools/" + tool):
				cairn.warn(("Failed to find program %s. " +
							"LVM volumes will not be handled") % tool)
				sysdef.info.setChild("env/tools/lvm", "False")
				return
		cairn.debug("lvm tools found")
		sysdef.info.setChild("env/tools/lvm", "True")
		return
