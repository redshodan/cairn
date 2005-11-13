"""cairn.sysdefs.darwin.__init__py
   Darwin (OS/X) system definitions"""


import sys
import re

import cairn
import cairn.Options
from cairn import sysdefs


def matchPlatform():
	if re.compile("[Dd]arwin").match(sys.platform):
		return True
	return False


def loadPlatform():
	platform = sysdefs.selectPlatform("cairn.sysdefs.darwin", [])
	platform.load()
	return platform
