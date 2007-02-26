"""templates.unix.archive.mergemeta.PrepMeta Module"""



import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.archive.write import PrepMeta as impl


def getClass():
	return PrepMeta()



class PrepMeta(impl.PrepMeta):

	def getDateAction(self):
		return "modified"


	def getInfo(self, sysdef):
		return sysdef.readInfo
