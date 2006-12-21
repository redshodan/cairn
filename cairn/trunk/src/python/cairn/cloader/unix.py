""" cairn.cloader.unix -- Unix specific code"""



import os
import imp
import stat



def prep(name):
	os.chmod(name, stat.S_IRWXU)
	imp.load_dynamic("pylibparted", name)
	return
