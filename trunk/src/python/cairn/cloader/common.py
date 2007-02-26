"""cairn.cloader.commmon"""


import os
import os.path
import re
import sys
import stat
import zipfile

import cairn


__pydir = None


def load(libname, path, modname):
	global __pydir
	try:
		if not __pydir:
			__pydir = cairn.mkdtemp("cairn-clib")
		zfile = zipfile.ZipFile(libname, "r")
		# Try: %.py, _%.so, %.so
		ret = loadFile(zfile, path, "%s.py" % modname)
		if ret: return ret
		ret = loadFile(zfile, path, "_%s.so" % modname)
		if ret: return ret
		ret = loadFile(zfile, path, "%s.so" % modname)
		if ret: return ret
		# Try regex match if direct matches failed
		names = zfile.namelist()
		name = findName(names, os.path.join(path, modname))
		if not name:
			raise cairn.Exception("Failed to find C library %s" % modname)
		ret = loadFile(zfile, path, name.split("/")[-1:][0])
		if ret: return ret
	except Exception, err:
		raise cairn.Exception("Failed loading C library from CAIRN shar file:",
							  err)
	return None


def findName(names, modname):
	exp = re.compile(modname)
	for name in names:
		if exp.search(name):
			return name
	return None


def loadFile(zfile, path, modname):
	global __pydir
	fulldir = __pydir
	zippath = os.path.join(path, modname)
	info = None
	try:
		info = os.lstat(fulldir)
	except:
		pass
	if path and not (info and stat.S_ISDIR(info[stat.ST_MODE])):
		os.makedirs(fulldir)
		# Throw in an empty __init__.py just in case
		f = file(os.path.join(fulldir, "__init__.py"), "w+")
		f.close()
	data = None
	try:
		data = zfile.read(zippath)
	except: pass
	if not data:
		return None
	try:
		ofile = file(os.path.join(fulldir, modname), "w+")
		ofile.write(data)
		ofile.close()
	except Exception, err:
		raise cairn.Exception("Failed to write C library to temporary directory",
							  err)
	return os.path.join(fulldir, modname)
