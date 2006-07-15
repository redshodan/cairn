"""templates.unix.extract.meta.edit.RunEditor Module"""



import os
import md5
import types

import cairn
from cairn import Options



def getClass():
	return RunEditor()



class RunEditor(object):

	def md5Meta(self, sysdef, meta):
		metaFile = file(meta, "r")
		md5sum = md5.new()
		while True:
			data = metaFile.read(512)
			if data:
				md5sum.update(data)
			else:
				break
		cairn.debug("MD5 of original meta: %s" % md5sum.hexdigest())
		return md5sum.hexdigest()


	def chooseEditor(self, sysdef):
		if type(Options.get("edit-meta")) == types.StringType:
			return Options.get("edit-meta")
		elif "EDITOR" in os.environ:
			return os.environ["EDITOR"]
		else:
			return "vi"


	def runEditor(self, sysdef, meta, editor):
		if os.system("%s %s" % (editor, meta)) != 0:
			raise cairn.Exception("Editor returned error when editing meta file. Image file not modified.")
		return


	def run(self, sysdef):
		meta = sysdef.info.get("archive/metafilename")
		orgMD5 = self.md5Meta(sysdef, meta)
		editor = self.chooseEditor(sysdef)
		self.runEditor(sysdef, meta, editor)
		newMD5 = self.md5Meta(sysdef, meta)
		if orgMD5 == newMD5:
			cairn.info("The meta file was not changed. Image file not modified.")
			sysdef.quit()
		return True
