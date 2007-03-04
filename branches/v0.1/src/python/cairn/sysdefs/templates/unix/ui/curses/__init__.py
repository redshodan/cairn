"""templates.unix.ui.curses Module"""



import logging

import cairn
from cairn import Options
from cairn import Logging






def getSubModuleString(sysdef):
	if Options.get("ui") == "curses":
		return "Init"
	else:
		return None



# Display console log messages using curses
class CursesHandler(logging.Handler):

	def flush(self):
		curses.doupdate()
		return


	def emit(self, record):
		displayStr(record.getMessage())
		return



def shutdown():
	global rootWin
	try:
		# Set everything back to normal
		rootWin.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
	except Exception, err:
		raise cairn.Exception("Failed to shutdown the curses interface",
							  err)
	return


def setCleanUpFunc():
	cairn.setUICleanUp(shutdown)
	return


def init():
	global rootWin
	rootWin = curses.initscr()
	curses.noecho()
	curses.cbreak()
	rootWin.keypad(1)
	try:
		curses.start_color()
	except:
		pass
	return

def initLogWin():
	global rootPanel
	global logWin
	(uly, ulx) = rootPanel.window().getbegyx()
	(height, width) = rootPanel.window().getmaxyx()
	logWin = rootPanel.window().subwin(height - 2, width - 2, uly + 1, ulx + 1)
	logWin.idlok(1)
	logWin.scrollok(1)
	cursToTop(logWin)
	#logWin.window().leaveok(1)
	return


def initLogging():
	Logging.display.setRootHandler(CursesHandler())


def displayStr(str):
	global logWin
	(height, width) = logWin.getmaxyx()
	#cursToTop(logWin)
	strlines = str.split("\n")
	strs = []
	for strline in strlines:
		count = len(strline) / width
		if len(strline) % width:
			count = count + 1
		iter = 0
		while iter < count:
			strs.append(strline[iter:iter * width + 1])
			iter = iter + 1
	logWin.addstr(str + "\n")
	flush()
	return


def flush():
	logWin.refresh()
	return
