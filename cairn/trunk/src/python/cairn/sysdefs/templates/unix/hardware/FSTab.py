"""templates.unix.hardware.FSTab Module"""


import os


def getClass():
	return FSTab()


class FSTab(object):
	def fstabFile(self):
		return "/etc/fstab"


	def run(self, sysdef):
		
		return True
