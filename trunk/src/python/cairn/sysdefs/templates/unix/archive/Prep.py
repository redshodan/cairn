"""templates.unix.archive.Prep Module"""


import os


import cairn
from cairn import Options



def getClass():
	return Prep()



class Prep(object):

	def run(self, sysdef):
		excludes = cairn.mktemp("cairn-excludes-")
		sysdef.info.setChild("archive/excludes-file", excludes[1])
		os.close(excludes[0])

		meta = cairn.mktemp("cairn-metadata-")
		sysdef.info.setChild("archive/metafilename", meta[1])
		os.close(meta[0])
		return True
