"""templates.unix.restore.setup.PartDrives Module"""


def getClass():
	return PartDrives()


class PartDrives(object):

	def partitionDrives(self, sysdef, drive):
		return


	def run(self, sysdef):
		cairn.log("Partitioning drives")
		for drive in sysdef.info.getElems("hardware/drive"):
			self.partitionDrive(sysdef, drive)
		return True
