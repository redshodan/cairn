"""templates.unix.restore.resolve.MatchDrives Module"""


def getClass():
	return MatchDrives()


class MatchDrives(object):

	def run(self, sysdef):
		return True
