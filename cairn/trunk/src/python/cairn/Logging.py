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

# Log objects
display = None
error = None
all = None


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
	# Redefine levels
	logging.addLevelName(DEVEL, "DEVEL")
	logging.addLevelName(DEBUG, "DEBUG")
	logging.addLevelName(VERBOSE, "VERBOSE")
	logging.addLevelName(INFO, "INFO")
	logging.addLevelName(WARNING, "WARNING")
	logging.addLevelName(ERROR, "ERROR")
	logging.addLevelName(CRITICAL, "CRITICAL")

	# all logger, always captures everything (except for devel, by default)
	cairn.Logging.all = Log("all", DEBUG,
							"%(asctime)s %(name)s %(levelname)s %(message)s",
							"%m-%d %H:%M")

	# display logger
	cairn.Logging.display = Log("display", INFO)
	cairn.Logging.display.setRootHandler(logging.StreamHandler(sys.stdout))
	cairn.Logging.display.setTargetHandler(all.logger, False)

	# error logger
	cairn.Logging.error = Log("error", WARNING)
	cairn.Logging.error.setRootHandler(logging.StreamHandler(sys.stderr))
	cairn.Logging.error.setTargetHandler(all.logger, False)

	cairn.Logging.all.log(INFO, "---------------------------------------")
	cairn.Logging.all.log(INFO, "Initialized CAIRN %s" % Version.toString())
	return


def setAllLogFile(filename):
	handler = logging.FileHandler(filename)
	cairn.Logging.all.setRootHandler(handler)
	cairn.Logging.all.setTargetHandler(handler, True)
	return


def setLogLevel(level):
	cairn.Logging.display.setLevel(level)
	if level > cairn.Logging.error.level:
		cairn.Logging.error.setLevel(level)
	if level == DEVEL:
		cairn.Logging.all.setLevel(level)
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
	else:
		return None
