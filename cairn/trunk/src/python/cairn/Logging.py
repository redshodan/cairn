"""cairn.Logging - Logging setup and handling"""


import sys
import logging

import cairn


# Log levels
DEBUG = logging.DEBUG
VERBOSE = logging.DEBUG + 10
INFO = logging.DEBUG + 20
WARNING = logging.DEBUG + 30
ERROR = logging.DEBUG + 40
CRITICAL = logging.DEBUG + 50

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
		self.logger.setLevel(DEBUG)
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
	logging.addLevelName(VERBOSE, "VERBOSE")
	logging.addLevelName(INFO, "INFO")
	logging.addLevelName(WARNING, "WARNING")
	logging.addLevelName(ERROR, "ERROR")
	logging.addLevelName(CRITICAL, "CRITICAL")

	# all logger, always captures everything
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
	return


def strToLogLevel(str):
	if str == "critical":
		return CRITICAL
	elif str == "error":
		return ERROR
	elif str == "warning":
		return WARNING
	elif str == "info":
		return INFO
	elif str == "verbose":
		return VERBOSE
	elif str == "debug":
		return DEBUG
	else:
		return None
