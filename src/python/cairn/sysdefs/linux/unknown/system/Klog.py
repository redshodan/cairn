"""linux.unknown.system.Klog Module"""


def getClass():
	return Klog()



class Klog(object):

	def run(self, sysdef):
		from cairn.sysdefs.linux.unknown.misc import klog
		klog.start()
		return True
