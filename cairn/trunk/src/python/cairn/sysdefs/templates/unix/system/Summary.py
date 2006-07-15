"""templates.unix.system.Summary Module"""


import cairn
from cairn import Options



def getClass():
	return Summary()



class Summary(object):

	def summary(self, sysdef):
		if Options.get("summary"):
			sysdef.printSummary()
			sysdef.quit()
		return


	def printMeta(self, sysdef):
		if Options.get("print-meta"):
			sysdef.printMeta()
			sysdef.quit()
		return


	def dumpMeta(self, sysdef):
		if Options.get("dumpenv"):
			fileName = sysdef.info.get("archive/metafilename")
			try:
				metafile = file(fileName, "w+")
				sysdef.info.saveToFile(metafile, True)
				metafile.close()
				sysdef.quit()
				cairn.log("Dumped environment metafile to: %s" % fileName)
			except Exception, err:
				raise cairn.Exception("Failed to write environment metadata to %s: %s" % \
									  (fileName, err))
		return


	def run(self, sysdef):
		self.summary(sysdef)
		self.printMeta(sysdef)
		self.dumpMeta(sysdef)
		return True
