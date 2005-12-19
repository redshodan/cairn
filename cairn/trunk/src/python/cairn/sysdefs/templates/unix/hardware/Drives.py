"""templates.unix.hardware.Drives Module"""


import os


def getClass():
	return Drives()


class Drives(object):
	def run(self, sysdef):
		return True
