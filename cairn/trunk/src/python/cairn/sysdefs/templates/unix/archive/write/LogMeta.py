"""templates.unix.archive.write.LogMeta Module"""


import cairn
from cairn import Options



def getClass():
	return LogMeta()



class LogMeta(object):

	def logMeta(self, sysdef):
		# The rest is logged in system.Summary
		strs = []
		strs.append(sysdef.info.getElem("archive").toPrettyStr([]))
		cairn.debug("Archive summary:\n%s" % "\n".join(strs))
		return


	def run(self, sysdef):
		self.logMeta(sysdef)
		return True
