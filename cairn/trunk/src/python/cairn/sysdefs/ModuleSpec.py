"""cairn.sysdefs.ModuleSpec - Module spcification string parser"""


#
# Syntax. Spaces are removed.
#
#   string -- Letters, numbers and '_'. ';' seperates words. '()' can combine words.
#
#   /pattern/string -- Replace regexp 'pattern' with 'string'
#   string1=string2 -- Replace 'string1' with 'string2'
#   string1<string2 -- Insert 'string2' before 'string1'
#   string1>string2 -- Insert 'string2' after 'string1'
#


import re
import string

import cairn
from cairn import Options


def parseModuleSpec(sysDef, moduleSpec, userModuleSpec, prefix):
	moduleNames = splitModuleSpec(moduleSpec, prefix)
	if userModuleSpec:
		userModuleNames = splitModuleSpec(userModuleSpec, None)
		applySpec(moduleNames, userModuleNames)
		# Recombine and split again, a word can now have multiple words.
		moduleSpec = ";".join(moduleNames)
		moduleNames = splitModuleSpec(moduleSpec, None)
	return moduleNames


def splitModuleSpec(moduleSpec, prefix):
	moduleNames = []
	for module in string.split(moduleSpec, ";"):
		module = string.replace(module, " ", "")
		if len(module) > 0:
			if prefix:
				moduleNames.append("%s.%s" % (prefix, module))
			else:
				moduleNames.append(module)
	return moduleNames


def applySpec(moduleNames, userModuleNames):
	for userModule in userModuleNames:
		if userModule.startswith("/"):
			applyRE(moduleNames, userModule)
		elif userModule.find("="):
			applyReplace(moduleNames, userModule)
		elif userModule.find("<") or userModule.find(">"):
			applyInsert(moduleNames, userModule)


def applyRE(moduleNames, userModule):
	userModule = userModule[1:len(userModule)]
	words = userModule.split("/")
	pattern = re.compile(words[0])
	for i, v in enumerate(moduleNames):
		if pattern.search(v):
			moduleNames[i] = words[1]
			break
	return


def applyReplace(moduleNames, userModule):
	words = userModule.split("=")
	for i, v in enumerate(moduleNames):
		if v == words[0]:
			moduleNames[i] = words[1]
			break
	return


def applyInsert(moduleNames, userModule):
	if userModule.find("<"):
		before = True
		words = userModule.split("<")
	else:
		before = False
		words = userModule.split(">")

	for i, v in enumerate(moduleNames):
		if v == words[0]:
			if before:
				moduleNames.insert(i, words[1])
			else:
				moduleNames.insert(i+1, words[1])
			break
	return
