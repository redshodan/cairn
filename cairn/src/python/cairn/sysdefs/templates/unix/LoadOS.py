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
		sysinfo.set("OS", self.nameOS())
		sysinfo.set("OS_VER", arr[0])
		sysinfo.set("OS_VER_SHORT", "%s.%s" % (nums[0], nums[1]))
		sysinfo.set("OS_VER_STR", release)
		sysinfo.set("OS_DISTRO", sysdef.name())
		return True
