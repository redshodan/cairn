"""templates.unix.archive.Excludes Module"""


import os
import re

import cairn
from cairn import Options



def getClass():
	return Excludes()



class Excludes(object):

	def cleanExclude(self, exclude):
		exclude = exclude.strip()
		return exclude.rstrip("/")


	def createExcludes(self, sysdef):
		if not Options.get("exclude"):
			return
		for exclude in Options.get("exclude").split(";"):
			exclude = self.cleanExclude(exclude)
			sysdef.info.createArchiveExcludesElem(exclude, "user")
		return


	def loadUserExcludesFile(self, sysdef):
		userFileName = sysdef.info.get("archive/user-excludes-file")
		if not userFileName:
			return
		userFile = None
		try:
			userFile = file(userFileName, "r")
		except Exception, err:
			raise cairn.Exception("Unable to open excludes file %s: %s" % \
								  (userFileName, err))
		for exclude in userFile:
			exclude = self.cleanExclude(exclude)
			sysdef.info.createArchiveExcludesElem(exclude, "user")
		userFile.close()
		return


	def excludeArchive(self, sysdef):
		sysdef.info.createArchiveExcludesElem(sysdef.info.get("archive/filename"),
											  "ignored_fs")
		return


	def loadFSExcludes(self, sysdef):
		return


	def createExcludesFile(self, sysdef):
		if not sysdef.info.getElem("archive/excludes"):
			return
		excludesFileName = sysdef.info.get("archive/excludes-file")
		try:
			path = re.split("/[^/]*$", excludesFileName)
			os.makedirs(path[0], 0700)
		except:
			pass
		try:
			excludesFile = file(excludesFileName, "w")
			cairn.addFileForCleanup(excludesFileName)
			for exclude in sysdef.info.getElems("archive/excludes/exclude"):
				excludesFile.write(exclude.getText())
				excludesFile.write("\n")
			excludesFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to open excludes file %s: %s" % (excludesFileName, err))
		return


	def run(self, sysdef):
		self.createExcludes(sysdef)
		self.loadUserExcludesFile(sysdef)
		self.excludeArchive(sysdef)
		self.loadFSExcludes(sysdef)
		self.createExcludesFile(sysdef)
		return True
