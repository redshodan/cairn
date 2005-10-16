"""Linux system definitions"""


import sys
import re

import cairn
import cairn.Options
from cairn import sysdefs


distros = ["redhat"]


def matchPlatform():
	if re.compile("[Ll]inux").match(sys.platform):
		return True
	return False


def loadPlatform():
	platform = sysdefs.selectPlatform("cairn.sysdefs.linux", distros)
	platform.load()
	return platform
