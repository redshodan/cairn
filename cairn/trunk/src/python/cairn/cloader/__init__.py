""" cairn.cloader -- C library loading functions """



import re

import cairn
import common



def load(sysdef, libname, path, modname):
	filename = common.load(libname, path, modname)
	if sysdef.getBaseType() == sysdef.UNIX:
		import unix
		unix.prep(modname, filename)
	else:
		raise cairn.Exception("Unknown system type while trying to import C library")
	return
