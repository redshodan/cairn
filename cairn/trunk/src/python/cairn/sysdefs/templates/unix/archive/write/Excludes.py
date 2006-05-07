"""templates.unix.archive.write.Excludes Module"""


import commands

import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.archive.Excludes as tmpl
from cairn.sysdefs.linux import Constants



def getClass():
	return Excludes()



class Excludes(tmpl.Excludes):
	None
