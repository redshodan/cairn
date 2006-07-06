"""templates.unix.readmeta.VerifyMeta Module"""



import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo
from cairn import Version



def getClass():
	return VerifyMeta()



class VerifyMeta(object):

	def verifyMeta(self, sysdef):
		if not sysdef.readInfo.verify():
			raise cairn.Exception("Invalid image file. Metadata failed verification.")
		return


	def verifyVersion(self, sysdef):
		major = int(sysdef.readInfo.get("version/major"))
		minor = int(sysdef.readInfo.get("version/minor"))
		svnrev = int(sysdef.readInfo.get("version/svnrev"))
		devel = sysdef.readInfo.get("version/devel")
		if ((major > Version.MAJOR) or
			((major == Version.MAJOR) and (minor > Version.MINOR))):
			raise cairn.Exception("Image file is from a newer version of CAIRN. This will most likely not work. Use --force if you wish to try anyways.")
		if ((not Version.DEVEL) and (devel == "True")):
			raise cairn.Exception("Image file is from a development version of CAIRN and this build of CAIRN is a release version. This will most likely not work. Use --force if you wish to try anyways.")
		return


	def run(self, sysdef):
		self.verifyMeta(sysdef)
		self.verifyVersion(sysdef)
		return True
