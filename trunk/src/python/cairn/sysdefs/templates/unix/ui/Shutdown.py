"""templates.unix.ui.Shutdown Module"""



import cairn
from cairn import Options



def getClass():
	return Shutdown()



class Shutdown(object):

	def run(self, sysdef):
		if Options.get("no-ui") or Options.get("ui") == "none":
			return True
		elif Options.get("ui") == "curses":
			sysdef.moduleList.insertAfterMe("ui.curses.Shutdown")
		return True
