"""templates.unix.restore.resolve.MatchDevices Module"""


def getClass():
	return MatchDevices()


class MatchDevices(object):

	def run(self, sysdef):
		return True
