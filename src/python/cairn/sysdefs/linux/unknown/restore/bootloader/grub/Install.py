"""linux.unknown.restore.bootloader.grub.Install Module"""


import os
import os.path

import cairn



def getClass():
	return Install()


class Install(object):

	def writeCmdFile(self, sysdef, cmdFileName):
		cmdFile = None
		try:
			cmdFile = file(cmdFileName, "w+")
		except Exception, err:
			raise cairn.Exception("Failed to open GRUB command file %s: %s" %
								  (cmdFileName, err))
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
		grub = grub.replace(sysdef.info.get("env/mountdir"), "")
		cmd = "%s %s %s --no-floppy --batch < %s" % (chroot, mdir, grub,
													 cmdFileName)
		cairn.run(cmd)
		return


	def cleanup(self, cmdFileName):
		try:
			os.remove(cmdFileName)
		except:
			pass
		return


	def run(self, sysdef):
		cairn.log("Installing GRUB")
		mdir = sysdef.info.get("env/mountdir")
		cmdFileName = os.path.join(mdir, "tmp/cairn-grub.cmd")
		self.writeCmdFile(sysdef, cmdFileName)
		self.runGrub(sysdef, mdir, cmdFileName)
		self.cleanup(cmdFileName)
		return True
