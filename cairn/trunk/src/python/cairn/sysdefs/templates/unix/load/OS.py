"""Generic unix.load.OS Module"""


import os



def getClass():
	return OS()



class OS(object):
	def nameOS(self):
		return "UNIX"


	def run(self, sysdef):
		sysname, nodename, release, version, machine = os.uname()
		arr = release.split("-")
		nums = arr[0].split(".")
		sysdef.info.set("os/name", self.nameOS())
		sysdef.info.set("os/version", arr[0])
		sysdef.info.set("os/version-short", "%s.%s" % (nums[0], nums[1]))
		sysdef.info.set("os/version-str", release)
		sysdef.info.set("os/distribution", sysdef.name())
		return True
