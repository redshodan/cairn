"""templates.unix.ui.curses.Init Module"""


import time
#import curses
from thirdparty import urwid
from thirdparty.urwid import curses_display


import cairn
from cairn.sysdefs.templates.unix.ui import curses as uic



def getClass():
	return Init()



class Init(object):

	def runold(self, sysdef):
		uic.setCleanUpFunc()
		try:
			uic.initCurses()
			uic.initRootPanel()
			uic.initLogWin()
			uic.initLogging()
		except Exception, err:
			raise cairn.Exception("Failed to initialize the curses interface:",
								  err)
		return True


	def run(self, sysdef):
		ui = curses_display.Screen()
		ui.init()
		cols, rows = ui.get_cols_rows()
		txt = urwid.Text("Hello World", align="center")
		fill = urwid.Filler( txt )
		canvas = fill.render( (cols, rows) )
		ui.draw_screen( (cols, rows), canvas )
		time.sleep(5)
		ui.deinit()
		return True
