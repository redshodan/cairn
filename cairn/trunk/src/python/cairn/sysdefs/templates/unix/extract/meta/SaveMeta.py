"""templates.unix.extract.meta.SaveMeta Module"""



import os.path

import cairn
from cairn import Options



def getClass():
	return SaveMeta()



class SaveMeta(object):

	def openMeta(self, filename):
		try:
			meta = file(filename, "w+")
			return meta
		except Exception, err:
			raise cairn.Exception("Failed to open metadata file: %s" % err)
		return


	def writeFile(self, sysdef, meta):
		try:
			sysdef.readInfo.saveToFile(meta, True)
			meta.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file: %s" % err)
		return


	def run(self, sysdef):
		saveMeta = Options.get("save-meta")
		if saveMeta:
			saveMeta = os.path.abspath(saveMeta)
			meta = self.openMeta(saveMeta)
			self.writeFile(sysdef, meta)
			cairn.display("Saved meta file to: %s" % saveMeta)
			sysdef.quit()
		return True
