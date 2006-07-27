"""cairn.CLoader"""


import os
import os.path
import re
import sys
import stat
import zipfile

import cairn


pydir = None


def load(libname, path, filename):
	try:
		if not cairn.CLoader.pydir:
			#cairn.CLoader.pydir = "/tmp/cairn-clib"
			#os.makedirs(cairn.CLoader.pydir)
			cairn.CLoader.pydir = cairn.mkdtemp("cairn-clib")
			#print "clib", cairn.CLoader.pydir
			#sys.path.append(cairn.CLoader.pydir)
			#os.environ["LD_LIBRARY_PATH"] = os.path.join(pydir, path)
			#print "LD", os.environ["LD_LIBRARY_PATH"]
		zfile = zipfile.ZipFile(libname, "r")
		names = zfile.namelist()
		# Try re match first, then a %.py and _%.so
		try:
			name = findName(names, filename)
			return loadFile(zfile, path, name.split("/")[-1:][0])
		except: pass
		return loadFile(zfile, path, "%s.py" % filename)
		return loadFile(zfile, path, "_%s.so" % filename)
	except Exception, err:
		raise cairn.Exception("Failed loading C library from CAIRN shar file:", err)
	return None


def findName(names, filename):
	exp = re.compile(filename)
	for name in names:
		if exp.search(name):
			return name
	raise cairn.Exception("Failed loading C library '%s' from CAIRN shar file" % filename)


def loadFile(zfile, path, filename):
	#if path:
	#	fulldir = os.path.join(cairn.CLoader.pydir, path)
	#else:
	fulldir = cairn.CLoader.pydir
	zippath = os.path.join(path, filename)
	info = None
	try:
		info = os.lstat(fulldir)
	except:
		pass
	if path and not (info and stat.S_ISDIR(info[stat.ST_MODE])):
		os.makedirs(fulldir)
		f = file(os.path.join(fulldir, "__init__.py"), "w+")
		f.close()
	data = zfile.read(zippath)
	ofile = file(os.path.join(fulldir, filename), "w+")
	ofile.write(data)
	ofile.close()
	return os.path.join(fulldir, filename)
