"""linux.unknown.system.partitions.FSTab Module"""


import re

import cairn
import cairn.sysdefs.templates.unix.system.partitions.FSTab as tmpl
from cairn.sysdefs.linux import Shared, Constants



def getClass():
	return FSTab()



class FSTab(tmpl.FSTab):

	def match(self, line):
		if Constants.FSTAB_UUID_RE.search(line):
			arr = line.split()
			return ("fs/uuid", arr[tmpl.DEVICE].lstrip("UUID="))
		elif Constants.FSTAB_LABEL_RE.search(line):
			arr = line.split()
			return ("fs/label", arr[tmpl.DEVICE].lstrip("LABEL="))
		else:
			return super(FSTab, self).match(line)
