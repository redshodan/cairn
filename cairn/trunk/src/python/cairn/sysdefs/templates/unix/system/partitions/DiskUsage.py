"""templates.unix.system.partitions.DiskUsage Module"""



def getClass():
	return DiskUsage()



class DiskUsage(object):
	def run(self, sysdef):
		return True
