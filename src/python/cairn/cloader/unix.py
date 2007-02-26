""" cairn.cloader.unix -- Unix specific code"""



import os
import imp
import stat



def prep(modname, filename):
	os.chmod(filename, stat.S_IRWXU)
	imp.load_dynamic(modname, filename)
	return
