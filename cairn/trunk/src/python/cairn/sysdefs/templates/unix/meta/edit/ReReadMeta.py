"""templates.unix.meta.edit.ReReadMeta Module"""



import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return ReReadMeta()



class ReReadMeta(object):

	def run(self, sysdef):
		meta = sysdef.info.get("archive/metafilename")
		sysdef.readInfo = SystemInfo.readNew(meta)
		return True
