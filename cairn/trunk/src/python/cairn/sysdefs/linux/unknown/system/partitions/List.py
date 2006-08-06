"""linux.unknown.system.partitions.List Module"""


import re


import cairn
import cairn.sysdefs.templates.unix.system.partitions.List as tmpl


def getClass():
	return List()


class List(tmpl.List):

	def run(self, sysdef):
		sysdef.moduleList.insertAfterMe("system.partitions.ListParted")
		return True
