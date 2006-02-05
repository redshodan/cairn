"""linux.unknown.copy.load.Paths Module"""


import cairn
import cairn.Options as Options
import cairn.sysdefs as sysdefs
import cairn.sysdefs.linux.unknown.load.Paths as tmpl
import cairn.sysdefs.linux.unknown.archive.Tools as Tools


def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		super(Paths, self).__init__()
		bins = { "env/tools/diskfree" : [sysdefs.PATH_REQUIRED, "df"],
				 "env/tools/diskusage" : [sysdefs.PATH_REQUIRED, "du"] }
		self.__BINS.update(bins)


	def run(self, sysdef):
		if not super(Paths, self).run(sysdef):
			return False
		self.chooseTool(sysdef, "archive", Tools.ARCHIVE)
		self.chooseTool(sysdef, "zip", Tools.ZIP)
		return True
