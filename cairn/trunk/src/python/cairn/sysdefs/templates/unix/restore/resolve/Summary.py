"""templates.unix.restore.resolve.Summary Module"""



import sys
import re
import time

import cairn
from cairn import Options



def getClass():
	return Summary()


class Summary(object):

	def display(self, sysdef):
		cairn.display("")
		cairn.display("Summary of actions that will be taken:")
		cairn.display("Image drives:")
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			cairn.display("  %s: size=%s model=%s" %
						  (drive.get("device"), drive.get("size"),
						   drive.get("model")))
		cairn.display("System drives:")
		for drive in sysdef.info.getElems("hardware/drive"):
			cairn.display("  %s: size=%s model=%s" %
						  (drive.get("device"), drive.get("size"),
						   drive.get("model")))
		cairn.display("Drive mapping (image -> system):")
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			cairn.display("  %s -> %s" % (drive.get("device"),
										  drive.get("mapped-device")))
		cairn.displayNL()
		# This needs more work before it'll be useful in the slightest
		#driveMatch = sysdef.readInfo.get("hardware/drive-match")
		#if driveMatch == "perfect":
		#	cairn.display("Drives were matched perfectly.")
		#elif driveMatch == "devices":
		#	cairn.display("Drives were not matched perfectly. Either a drives size or model did not exactly match.")
		#elif driveMatch == "partial":
		#	cairn.display("Drives were matched partially. Either device names were different or the number of drives did not match")
		#elif driveMatch == "none":
		#	cairn.display("Drives were not matched at all.")
		return


	def warn(self, sysdef):
		cairn.display("***********************************************************************")
		cairn.display("You have 10 seconds to press ctrl-C if you wish to stop this restore")
		cairn.display("***********************************************************************")
		cairn.displayNL()
		time.sleep(10)
		return


	def ask(self, sysdef):
		cairn.displayRaw("Do you wish to continue with this restore? [y/N]: ")
		line = sys.stdin.readline()
		cairn.displayNL()
		if re.match("[yY]", line):
			return True
		else:
			cairn.display("Canceling restore")
			return False


	def run(self, sysdef):
		self.display(sysdef)
		if Options.get("pretend"):
			sysdef.quit()
		elif Options.get("batch"):
			self.warn(sysdef)
		else:
			if not self.ask(sysdef):
				sysdef.quit()
		return True
