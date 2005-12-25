"""templates.unix.hardware.Partitions Module"""


import os


def getClass():
	return Partitions()


class Partitions(object):
	def run(self, sysdef):
		return True
