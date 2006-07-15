"""templates.unix.archive.write.PrepMeta Module"""



import cairn
from cairn import Options



def getClass():
	return PrepMeta()



class PrepMeta(object):

	def getDateAction(self):
		return "created"


	def getInfo(self, sysdef):
		return sysdef.info


	def setDate(self, sysdef):
		self.getInfo(sysdef).createDatesDateElem(self.getDateAction())
		return


	def run(self, sysdef):
		self.setDate(sysdef)
		return True
