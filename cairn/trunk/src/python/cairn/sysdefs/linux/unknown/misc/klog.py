"""linux.unknown.misc.klog"""



import re
import time
import threading
import klogctl

import cairn
from cairn import Options


__prevLines = []
__consoleDisabled = False
__compareDepth = 5


class KlogThread(threading.Thread):

	def __init__(self):
		self.__lock = threading.Lock()
		self.__running = True
		super(KlogThread, self).__init__()
		return


	def stop(self):
		self.__lock.acquire()
		self.__running = False
		self.__lock.release()
		return


	def run(self):
		init()
		self.__lock.acquire()
		while self.__running:
			self.__lock.release()
			pollKlog()
			time.sleep(0.5)
			self.__lock.acquire()
		self.__lock.release()
		deinit()
		return


# Main entry point
def start():
	thread = KlogThread()
	cairn.registerThread(thread)
	thread.start()
	return


def init():
	global __prevLines
	if Options.get("command") == "restore":
		disableConsoleMsgs()
	__prevLines = getLogLines()
	return


def deinit():
	enableConsoleMsgs()
	return


def disableConsoleMsgs():
	global __consoleDisabled
	__consoleDisabled = True
	klogctl.klogctl(6, 0)
	return


def enableConsoleMsgs():
	global __consoleDisabled
	if __consoleDisabled:
		__consoleDisabled = False
		klogctl.klogctl(7, 0)
	return


def getLogLines():
	size = klogctl.klogctl(10, 0)
	buf = klogctl.klogctl(3, 32768)
	lines = buf.split("\n")
	# Skip truncated starting line
	if not re.match("$<[0-9]>", lines[0]):
		lines = lines[1:]
	if not lines[-1]:
		del lines[-1]
	return lines


def reverse(array):
	rarray = []
	for pos in xrange(1, len(array)+1):
		rarray.append(array[-pos])
	return rarray


# Compare __compareDepth worth of lines backward trying to find where previous
# messages match up the current messages and log the difference
def pollKlog():
	global __prevLines, __compareDepth
	lines = getLogLines()
	prev = reverse(__prevLines[-(__compareDepth + 1):])
	for pos in xrange(1, len(lines) + 1):
		if pos == 1:
			cur = reverse(lines[-(__compareDepth + pos):])
		else:
			cur = reverse(lines[-(__compareDepth + pos):-(pos - 1)])
		match = True
		for p,c in zip(prev, cur):
			if p != c:
				match = False
				break
		if match:
			if pos > 1:
				for line in lines[-(pos - 1):]:
					cairn.verbose("printk: %s" % line[3:])
				__prevLines = lines
			return
	return
