"""linux.unknown.restore.bootloader.grub.Install Module"""


import os
import os.path
import commands

import cairn



def getClass():
	return Install()


class Install(object):

	def writeCmdFile(self, sysdef, cmdFileName):
		cmdFile = None
		try:
			cmdFile = file(cmdFileName, "w+")
		except Exception, err:
			raise cairn.Exception("Failed to open GRUB command file %s: %s" % (cmdFileName, err))
		cairn.addFileForCleanup(cmdFileName)
		cmdFile.write("root=%s\n" %
					  sysdef.info.get("machine/bootloader/partition"))
		cmdFile.write("setup %s\n" %
					  sysdef.info.get("machine/bootloader/drive"))
		cmdFile.write("quit\n")
		cmdFile.close()
		return


	def runGrub(self, sysdef, mdir, cmdFileName):
		chroot = sysdef.info.get("env/tools/chroot")
		grub = sysdef.info.get("env/tools/grub")
		cmd = "%s %s %s --no-floppy --batch < %s" % (chroot, mdir, grub, cmdFileName)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			raise cairn.Exception("Failed to run %s: %s" % (grub, err))
		cairn.log(ret[1])
		return


	def run(self, sysdef):
		cairn.log("Installing GRUB")
		mdir = sysdef.info.get("env/mountdir")
		cmdFileName = os.path.join(mdir, "tmp/cairn-grub.cmd")
		self.writeCmdFile(sysdef, cmdFileName)
		self.runGrub(sysdef, mdir, cmdFileName)
		return True
