"""templates.unix.extract.meta.Save Module"""



import os.path

import cairn
from cairn import Options



def getClass():
	return Save()



class Save(object):

	def openMeta(self, filename):
		try:
			meta = file(filename, "w+")
			return meta
		except Exception, err:
			raise cairn.Exception("Failed to open metadata file", err)
		return


	def writeFile(self, sysdef, meta):
		try:
			meta.write(sysdef.readInfo.toStr(True))
			meta.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		saveMeta = Options.get("save-meta")
		saveMeta = os.path.abspath(saveMeta)
		meta = self.openMeta(saveMeta)
		self.writeFile(sysdef, meta)
		cairn.display("Saved metadata to: %s" % saveMeta)
		return True
