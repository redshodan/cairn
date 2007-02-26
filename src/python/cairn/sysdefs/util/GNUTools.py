"""cairn.sysdefs.utils.GNUTools"""



import re

import cairn


def verifyToolsExit(archiveTool, zipTool):
	if (archiveTool.exit() == 0) and (zipTool.exit() == 0):
		return True
	if zipTool.exit() != 0:
		return False
	if len(archiveTool.err) == 0:
		return False
	str = archiveTool.err.strip()
	future = re.compile(".*time stamp.*is.*in the future.*")
	old = re.compile(".*implausibly old time stamp.*")
	verify = True
	for line in str.split("\n"):
		line = line.strip()
		if len(line) == 0:
			continue
		if future.match(line):
			continue
		if old.match(line):
			continue
		verify = False
		break
	return verify
