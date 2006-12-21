""" cairn.cloader -- C library loading functions """



import re

import cairn
import common



def load(sysdef, libname, path, filename):
	name = common.load(libname, path, filename)
	if sysdef.getBaseType() == sysdef.UNIX:
		import unix
		unix.prep(name)
	else:
		raise cairn.Exception("Unknown system type while trying to import C library")
	return
