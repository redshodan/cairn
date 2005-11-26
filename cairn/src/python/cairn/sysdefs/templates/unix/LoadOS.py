"""Generic UNIX LoadOS Module"""


import os



def getClass():
	return LoadOS()



class LoadOS(object):
	def nameOS(self):
		return "UNIX"


	def run(self, sysdef, sysinfo):
		sysname, nodename, release, version, machine = os.uname()
		arr = release.split("-")
		nums = arr[0].split(".")
		sysinfo.set("os/name", self.nameOS())
		sysinfo.set("os/version", arr[0])
		sysinfo.set("os/version-short", "%s.%s" % (nums[0], nums[1]))
		sysinfo.set("os/version-str", release)
		sysinfo.set("os/distribution", sysdef.name())
		return True
