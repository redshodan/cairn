"""linux.unknown.system.Paths Module"""



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
						Tool("vgcfgbackup", "env/tools/vgcfgbackup", False),
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
		for tool in Constants.LVM_TOOLS:
			self.__BINS.append(Tool(tool, "env/tools/" + tool, False))
		return


	def userCheck(self, sysdef):
		self.checkMD(sysdef)
		self.checkLVM(sysdef)
		return


	def checkMD(self, sysdef):
		if Options.get("no-raid"):
			return
		# Check for 
		if not sysdef.info.get("env/tools/mdadm"):
			cairn.warn("Failed to find program mdadm. Software RAIDs will " +
					   "not be handled.")
			sysdef.info.setChild("env/tools/md", "False")
		else:
			cairn.debug("mdadm found")
			sysdef.info.setChild("env/tools/md", "True")
		return


	def checkLVM(self, sysdef):
		if Options.get("no-lvm"):
			return
		# Check for 
		for tool in Constants.LVM_TOOLS:
			if not sysdef.info.get("env/tools/" + tool):
				cairn.warn(("Failed to find program %s. " +
							"LVM volumes will not be handled") % tool)
				sysdef.info.setChild("env/tools/lvm", "False")
				return
		cairn.debug("lvm tools found")
		sysdef.info.setChild("env/tools/lvm", "True")
		return
