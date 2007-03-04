"""templates.unix.system.Summary Module"""


import cairn
from cairn import Options



def getClass():
	return Summary()



class Summary(object):

	def logSummary(self, sysdef):
		strs = []
		strs.append(sysdef.info.getElem("os").toPrettyStr([]))
		strs.append(sysdef.info.getElem("arch").toPrettyStr([]))
		strs.append(sysdef.info.getElem("machine").toPrettyStr([]))
		strs.append(sysdef.info.getElem("env").toPrettyStr([]))
		strs.append(sysdef.info.getElem("hardware").toPrettyStr([]))
		cairn.debug("System summary:\n%s" % "\n".join(strs))
		return


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
				metafile.write(sysdef.info.toStr(True))
				metafile.close()
				sysdef.quit()
				cairn.log("Dumped environment metafile to: %s" % fileName)
			except Exception, err:
				raise cairn.Exception("Failed to write environment metadata to %s: %s" % \
									  (fileName, err))
		return


	def run(self, sysdef):
		self.logSummary(sysdef)
		self.summary(sysdef)
		self.printMeta(sysdef)
		self.dumpMeta(sysdef)
		return True
