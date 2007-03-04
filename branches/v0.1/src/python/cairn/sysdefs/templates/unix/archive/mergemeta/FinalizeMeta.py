"""templates.unix.archive.write.FinalizeMeta Module"""


import cairn
import cairn.sysdefs.templates.unix.archive.write.FinalizeMeta as tmpl



def getClass():
	return FinalizeMeta()



class FinalizeMeta(tmpl.FinalizeMeta):

	def md5sum(self, sysdef, archive):
		return sysdef.readInfo.get("archive/md5sum")


	def run(self, sysdef):
		tmpl.FinalizeMeta.run(self, sysdef)
		cairn.log("Metadata saved to image file")
		return True
