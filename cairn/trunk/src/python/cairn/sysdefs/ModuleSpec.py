"""cairn.sysdefs.ModuleSpec - Module specification string parser"""


#
# Syntax. Spaces are removed.
#
#   string -- Letters, numbers and '_'. ';' seperates words. '()' can combine words.
#             Nested '()' are not allowed.
#
#   /pattern/string -- Replace regexp 'pattern' with 'string'
#   string1=string2 -- Replace 'string1' with 'string2'
#   string1<string2 -- Insert 'string2' before 'string1'
#   string1>string2 -- Insert 'string2' after 'string1'
#   -string         -- Remove 'string' from the default
#   ^string         -- Prepend 'string' onto the default
#   $string         -- Append 'string' onto the default
#


import re
import string

import cairn
from cairn import Options


def parseModuleSpec(sysdef, moduleSpec, userModuleSpec, prefix):
	moduleNames = splitModuleSpec(moduleSpec, prefix)
	if userModuleSpec:
		userModuleNames = splitModuleSpec(userModuleSpec, None)
		applySpec(moduleNames, userModuleNames)
		# Recombine and split again, a word can now have multiple words.
		moduleSpec = ";".join(moduleNames)
		moduleNames = splitModuleSpec(moduleSpec, None)
	return moduleNames


def splitModuleSpec(moduleSpec, prefix):
	# First check for ()'s
	largeWords = []
	if (moduleSpec.find("(") >= 0) and (moduleSpec.find(")") >= 0):
		for largeWord in re.split("\(*\)", moduleSpec):
			largeWords.append(largeWord)
	else:
		largeWords.append(moduleSpec)

	moduleNames = []
	for largeWord in largeWords:
		if largeWord.find("(") >= 0:
			applyPrefix(moduleNames, largeWord.replace("(", ""), prefix)
		else:
			for module in string.split(largeWord, ";"):
				applyPrefix(moduleNames, module, prefix)
	return moduleNames


def applyPrefix(moduleNames, module, prefix):
	module = string.replace(module, " ", "")
	if len(module) > 0:
		if prefix:
			moduleNames.append("%s.%s" % (prefix, module))
		else:
			moduleNames.append(module)
	return


def applySpec(moduleNames, userModuleNames):
	for userModule in userModuleNames:
		if userModule.startswith("/"):
			applyRE(moduleNames, userModule)
		elif (userModule.find("=") >= 0):
			applyReplace(moduleNames, userModule)
		elif (userModule.find("<") >= 0) or (userModule.find(">") >= 0):
			applyInsert(moduleNames, userModule)
		elif (userModule.find("-") >= 0):
			applyRemove(moduleNames, userModule)
		elif (userModule.find("^") >= 0):
			applyPrepend(moduleNames, userModule)
		elif (userModule.find("$") >= 0):
			applyAppend(moduleNames, userModule)


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
	if (userModule.find("<") >= 0):
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


def applyRemove(moduleNames, userModule):
	try:
		moduleNames.remove(userModule[1:])
	except ValueError:
		pass
	return


def applyPrepend(moduleNames, userModule):
	moduleNames.insert(0, userModule[1:])
	return


def applyAppend(moduleNames, userModule):
	moduleNames.append(userModule[1:])
	return
