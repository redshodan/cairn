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
__display = None
__error = None
__all = None
__nolog = False
__isShutdown = False
__filename = None


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
		elif enabled():
			# Only store if we expect to get a log file set
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
		if isShutdown():
			if level >= INFO:
				print logging.getLevelName(level), msg
			return
		else:
			return self.logger.log(level, msg)


def enabled():
	global __nolog
	return not __nolog


def isShutdown():
	global __isShutdown
	return __isShutdown


def init():
	global __display, __error, __all, __nolog

	# Redefine levels
	logging.addLevelName(DEVEL, "DEVEL")
	logging.addLevelName(DEBUG, "DEBUG")
	logging.addLevelName(VERBOSE, "VERBOSE")
	logging.addLevelName(INFO, "INFO")
	logging.addLevelName(WARNING, "WARNING")
	logging.addLevelName(ERROR, "ERROR")
	logging.addLevelName(CRITICAL, "CRITICAL")

	# all logger, always captures everything (except for devel, by default)
	__all = Log("all", DEBUG, "%(asctime)s %(name)s %(levelname)s %(message)s",
			  "%m-%d %H:%M")

	# __display logger
	__display = Log("display", INFO)
	__display.setRootHandler(logging.StreamHandler(sys.stdout))
	__display.setTargetHandler(__all.logger, False)

	# __error logger
	__error = Log("error", WARNING)
	__error.setRootHandler(logging.StreamHandler(sys.stderr))
	__error.setTargetHandler(__all.logger, False)

	__all.log(INFO, "---------------------------------------")
	__all.log(INFO, "Initialized CAIRN %s" % Version.toString())
	return


def shutdown():
	global __isShutdown
	__isShutdown = True
	logging.shutdown()
	return


def getAllLogFile():
	global __nolog, __filename
	if __nolog:
		return None
	else:
		return __filename


def setAllLogFile(filename):
	global __all, __nolog, __filename
	if __nolog:
		return
	__filename = filename
	handler = logging.FileHandler(filename)
	__all.setRootHandler(handler)
	__all.setTargetHandler(handler, True)
	return


def setLogLevel(level):
	global __display, __error, __all, __nolog
	if level == NOLOG:
		__nolog = True
		return
	__display.setLevel(level)
	if level > __error.level:
		__error.setLevel(level)
	if level == DEVEL:
		__all.setLevel(level)
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


# Log pass through functions
def critical(msg, *args):
	global __error
	return __error.log(CRITICAL, "Critical: %s" % msg)


def error(msg, *args):
	global __error
	return __error.log(ERROR, "Error: %s" % msg)


def warn(msg, *args):
	global __error
	return __error.log(WARNING, "Warning: %s" % msg)


def info(msg, *args):
	global __display
	return __display.log(INFO, "%s" % msg)


def verbose(msg, *args):
	global __display
	return __display.log(VERBOSE, "%s" % msg)


def debug(msg, *args):
	global __display
	return __display.log(DEBUG, "%s" % msg)

def devel(msg, *args):
	global __display
	return __display.log(DEVEL, "%s" % msg)


def log(msg, *args):
	global __display
	return __display.log(INFO, "%s" % msg)


def allLog(level, msg):
	global __all
	return __all.log(level, "%s" % msg)


def display(msg):
	global __display
	return __display.log(INFO, "%s" % msg)


def displayRaw(msg, dolog = True):
	global __all
	if dolog:
		__all.log(INFO, "%s" % msg)
	print msg,
	sys.stdout.flush()
	return


def displayNL():
	print
	return
