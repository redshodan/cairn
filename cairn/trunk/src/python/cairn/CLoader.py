"""cairn.CLoader"""


import os
import os.path
import sys
import zipfile

import cairn


pydir = None


class CLoader(object):

	def load(self, libname, path, filename):
		if not cairn.CLoader.pydir:
			cairn.CLoader.pydir = cairn.mkdtemp("cairn-clib")
			sys.path.append(cairn.CLoader.pydir)
		zfile = zipfile.ZipFile(libname, "r")
		self.loadFile(zfile, path, "%s.py" % filename)
		self.loadFile(zfile, path, "_%s.so" % filename)
		return


	def loadFile(self, zfile, path, filename):
		ofile = file(os.path.join(cairn.CLoader.pydir, filename), "w+")
		ofile.write(zfile.read(os.path.join(path, filename)))
		ofile.close()
		return

