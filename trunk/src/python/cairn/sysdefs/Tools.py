"""cairn.sysdefs.Tools"""


import os

import cairn
from cairn import Options
from cairn.sysdefs import IModule



class Tool(object):
	def __init__(self, tool, tag, required):
		self.tool = tool
		self.tag = tag
		self.required = required



class ToolGroup(object):
	def __init__(self, tag, userChoiceTag, userOption, required, tools):
		self.tools = tools
		self.tag = tag
		self.userChoiceTag = userChoiceTag
		self.userOption = userOption
		self.required = required



def findTools(sysdef, path, toolList):
	"""Finds the binaries in the bins map using the path supplied"""
	sysdef.info.setChild("env/path", path)
	for entry in toolList:
		if isinstance(entry, Tool):
			found = IModule.findFileInPath(path, entry.tool)
			if found:
				sysdef.info.setChild(entry.tag, found)
		else:
			first = None
			for tool in entry.tools:
				bin = IModule.findFileInPath(path, tool.tool)
				if bin:
					sysdef.info.setChild(tool.tag, bin)
					if not first:
						first = tool
				else:
					sysdef.info.clear(tool.tag)
			if first:
				sysdef.info.setChild(entry.tag, first.tag)
			chooseTool(sysdef, entry)
		# Verify it was found
		if (not sysdef.info.get(entry.tag) and entry.required):
			sysdef.info.printSummary()
			raise cairn.Exception("Failed to find required binary: %s" % \
								  entry.tool, cairn.ERR_BINARY)
	return True


def chooseTool(sysdef, group):
	method = None
	userMethod = Options.get(group.userOption)
	if userMethod:
		for tool in group.tools:
			if userMethod == tool.tool:
				if sysdef.info.get(tool.tag):
					method = tool.tag
				else:
					raise cairn.Exception("%s type %s selected but was not found" % (group.userOption.capitalize(), userMethod))
		if not method:
			raise cairn.Exception("Invalid %s type selected: %s" % \
								  (group.userOption, userMethod))
	else:
		method = sysdef.info.get(group.tag)
	if method:
		sysdef.info.setChild(group.userChoiceTag, method)
	else:
		msg = "No %s types were found. Possible types: " % group.userOption
		for tool in group.tools:
			msg = msg + tool.tool + ","
		if msg.endswith(","):
			msg = msg[0 : len(msg) - 1]
		raise cairn.Exception(msg)
	return
