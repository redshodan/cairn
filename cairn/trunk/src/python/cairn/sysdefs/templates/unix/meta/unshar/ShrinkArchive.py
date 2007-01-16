"""templates.unix.archive.meta.unshar.ShrinkMeta Module"""



import cairn.sysdefs.templates.unix.archive.mergemeta.WriteMeta as tmpl
import cairn



def getClass():
	return ShrinkArchive()



class ShrinkArchive(tmpl.WriteMeta):

	def includeMeta(self):
		return False


	def userMsg(self):
		cairn.info("Removing metadata from image, this can take a long time")
		return
