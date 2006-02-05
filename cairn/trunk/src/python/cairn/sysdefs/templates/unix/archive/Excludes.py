"""templates.unix.archive.Excludes Module"""


import cairn
from cairn import Options



def getClass():
	return Excludes()



class Excludes(object):

	def addExcludes(self, iter, excludes):
		for exclude in iter:
			exclude = exclude.strip()
			exclude = exclude.rstrip("/")
			excludes[exclude] = True


	def createExcludes(self, sysdef, excludes):
		if not Options.get("exclude"):
			return
		self.addExcludes(Options.get("exclude").split(";"), excludes)
		return


	def loadUserExcludesFile(self, sysdef, excludes):
		userFileName = sysdef.info.get("archive/user-excludes-file")
		if not userFileName:
			return
		userFile = None
		try:
			userFile = file(userFileName, "r")
		except Exception, err:
			raise cairn.Exception("Unable to open excludes file %s: %s" % (userFileName,
																		   err))
		self.addExcludes(userFile, excludes)
		userFile.close()
		return


	def loadFSExcludes(self, sysdef, excludes):
		return


	def setMetaExcludes(self, sysdef, excludes):
		line = None
		for exclude, trash in excludes.iteritems():
			if line:
				line = line + ";" + exclude
			else:
				line = exclude
		if line:
			sysdef.info.set("archive/excludes", line)
		return


	def createExcludesFile(self, sysdef, excludes):
		if not sysdef.info.get("archive/excludes"):
			return
		excludesFileName = sysdef.info.get("archive/excludes-file")
		try:
			excludesFile = file(excludesFileName, "w")
			for exclude in sysdef.info.get("archive/excludes").split(";"):
				excludesFile.write(exclude)
				excludesFile.write("\n")
			excludesFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to open excludes file %s: %s" % (excludesFileName, err))
		return


	def run(self, sysdef):
		excludes = {}
		self.createExcludes(sysdef, excludes)
		self.loadUserExcludesFile(sysdef, excludes)
		self.loadFSExcludes(sysdef, excludes)
		self.setMetaExcludes(sysdef, excludes)
		self.createExcludesFile(sysdef, excludes)
		return True
