"""templates.unix.restore.setup.MatchDrives Module"""


def getClass():
	return MatchDrives()


class MatchDrives(object):

	def run(self, sysdef):
		return True
