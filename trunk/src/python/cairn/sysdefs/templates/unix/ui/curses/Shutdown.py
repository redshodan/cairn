"""templates.unix.ui.curses.Shutdown Module"""


import curses

import cairn
from cairn.sysdefs.templates.unix.ui import curses as uic



def getClass():
	return Shutdown()



class Shutdown(object):

	def run(self, sysdef):
		uic.shutdown()
		return True
