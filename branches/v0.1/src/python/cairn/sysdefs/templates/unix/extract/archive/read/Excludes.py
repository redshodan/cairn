"""templates.unix.extract.archive.read.Excludes Module"""


def getClass():
	return Excludes()


# No-op for extraction


class Excludes(object):

	def run(self, sysdef):
		return True
