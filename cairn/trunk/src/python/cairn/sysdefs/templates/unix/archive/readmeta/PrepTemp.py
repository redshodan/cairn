"""templates.unix.readmeta.PrepTemp Module"""



import os
import os.path
import tempfile

import cairn
from cairn import Options



def getClass():
	return PrepTemp()



class PrepTemp(object):

	def run(self, sysdef):
		tmpDir = tempfile.mkdtemp(None, "cairn-restore-")
		cairn.addFileForCleanup(tmpDir)
		sysdef.info.setChild("env/tmpdir", tmpDir)
		return true
