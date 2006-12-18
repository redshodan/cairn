"""cairn.Logging - Logging setup and handling"""


import sys
import logging

import cairn
from cairn import Version


# Log levels
DEVEL = 10
DEBUG = DEVEL + 10
VERBOSE = DEBUG + 10
INFO = VERBOSE + 10
WARNING = INFO + 10
ERROR = WARNING + 10
CRITICAL = ERROR + 10
NOLOG = -1

# Log objects
display = None
error = None
all = None
nolog = None


# Defer log messages to other handlers, queueing until handler set
class DeferHandler(logging.Handler):

	def init(self):
		self.__isLoopBack = False
		self.__target = None
		self.__buff = []
		return


	def setTargetHandler(self, target, isLoopBack):
		self.__target = target
		self.flush()
		self.__isLoopBack = isLoopBack
		return


	def flush(self):
		if self.__target and len(self.__buff):
			for buffered in self.__buff:
				self.__target.handle(buffered)
			del self.__buff[:]
		return


	def emit(self, record):
		if self.__isLoopBack:
			return
		if self.__target:
			return self.__target.handle(record)
		else:
			self.__buff.append(record)
		return



class Log(object):

	def __init__(self, name, level, format = None, dateFormat = None):
		self.name = name
		self.logger = logging.getLogger(name)
		self.level = level
		self.format = format
		self.dateFormat = dateFormat
		self.defer = DeferHandler()
		self.defer.init()
		self.rootHandler = None
		self.targetHandler = None
		self.logger.setLevel(DEVEL)
		self.logger.addHandler(self.defer)
		return


	def setRootHandler(self, handler):
		self.rootHandler = handler
		handler.setLevel(self.level)
		handler.setFormatter(logging.Formatter(self.format, self.dateFormat))
		self.logger.addHandler(handler)
		return


	def setTargetHandler(self, handler, isLoopBack):
		self.targetHandler = handler
		self.defer.setTargetHandler(handler, isLoopBack)
		return


	def setLevel(self, level):
		self.level = level
		if self.rootHandler:
			self.rootHandler.setLevel(level)
		return


	def log(self, level, msg):
		self.logger.log(level, msg)


def init():
	global display, error, all

	# Redefine levels
	logging.addLevelName(DEVEL, "DEVEL")
	logging.addLevelName(DEBUG, "DEBUG")
	logging.addLevelName(VERBOSE, "VERBOSE")
	logging.addLevelName(INFO, "INFO")
	logging.addLevelName(WARNING, "WARNING")
	logging.addLevelName(ERROR, "ERROR")
	logging.addLevelName(CRITICAL, "CRITICAL")

	# all logger, always captures everything (except for devel, by default)
	all = Log("all", DEBUG, "%(asctime)s %(name)s %(levelname)s %(message)s",
			  "%m-%d %H:%M")

	# display logger
	display = Log("display", INFO)
	display.setRootHandler(logging.StreamHandler(sys.stdout))
	display.setTargetHandler(all.logger, False)

	# error logger
	error = Log("error", WARNING)
	error.setRootHandler(logging.StreamHandler(sys.stderr))
	error.setTargetHandler(all.logger, False)

	all.log(INFO, "---------------------------------------")
	all.log(INFO, "Initialized CAIRN %s" % Version.toString())
	return


def setAllLogFile(filename):
	global all, nolog
	if nolog:
		return
	handler = logging.FileHandler(filename)
	all.setRootHandler(handler)
	all.setTargetHandler(handler, True)
	return


def setLogLevel(level):
	global display, error, all, nolog
	if level == NOLOG:
		nolog = True
		return
	display.setLevel(level)
	if level > error.level:
		error.setLevel(level)
	if level == DEVEL:
		all.setLevel(level)
	return


def strToLogLevel(str):
	if cairn.matchName("critical", str):
		return CRITICAL
	elif cairn.matchName("error", str):
		return ERROR
	elif cairn.matchName("warning", str):
		return WARNING
	elif cairn.matchName("info", str):
		return INFO
	elif cairn.matchName("verbose", str):
		return VERBOSE
	elif cairn.matchName("debug", str):
		return DEBUG
	elif cairn.matchName("devel", str):
		return DEVEL
	elif cairn.matchName("none", str):
		return NOLOG
	else:
		return None
