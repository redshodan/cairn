"""cairn.sysdefs.ModuleSpec - Module specification string parser"""


#
# Syntax. Spaces are removed.
#
#   string -- Letters, numbers and '_'. ';' seperates words. '""' can combine
#             words. Nested '""' are not allowed. Wrapping '/' around the
#             lefthand string turns it into a regular expression. Wrapping
#             '{}' around the right hand string turns it into code that is
#             inserted into a module template and placed into the list.
#
#   string(arg1=val1, arg2=val2, ...) -- Give a module these parameters
#   string1=string2 -- Replace 'string1' with 'string2'
#   string1<string2 -- Insert 'string2' before 'string1'
#   string1>string2 -- Insert 'string2' after 'string1'
#   -string         -- Remove 'string' from the default
#   ^string         -- Prepend 'string' onto the default
#   $string         -- Append 'string' onto the default
#


import re
import string
import shlex

import cairn
from cairn import Options


# Node Type
UNKNOWN = 0
IDENTIFIER = 1
USER_MOD_PY = 2
USER_MOD_SHELL = 3
MOD_PARAMS = 4
REGEX = 5

# Node Op Type
UNARY = 1
BINARY = 2
NO_OP = 3

# Operators
BINARY_OPS = ["=", "<", ">"];
UNARY_OPS = ["-", "^", "$"];

QUOTES = ["\"", "'", "/", "?"]
ASYM_QUOTES = ["(", ")", "{", "}", "[", "]"]
ASYM_QUOTES_LHS = ["(", "{", "["]
ASYM_QUOTES_RHS = [")", "}", "]"]
QUOTES_GROUPED = {")":"(", "}":"{", "]":"[", "\"":"\"", "'":"'", "/":"/",
				  "?":"?"}


class ModuleInfo(object):
	def __init__(self, **args):
		self.type = None
		self.opType = None
		self.lhs = None
		self.rhs = None
		self.op = None
		self.regex = None
		self.name = None
		self.module = None
		self.args = {}

		if "type" in args:
			self.type = args["type"]
		if "opType" in args:
			self.opType = args["opType"]
		if "lhs" in args:
			self.lhs = args["lhs"]
		if "rhs" in args:
			self.rhs = args["rhs"]
		if "op" in args:
			self.op = args["op"]
		if "regex" in args:
			self.regex = args["regex"]
		if "name" in args:
			self.name = args["name"]
		if "module" in args:
			self.module = args["module"]
		if "args" in args:
			self.args = args["args"]
		return


	def copy(self, rhs):
		self.type = rhs.type
		self.opType = rhs.opType
		self.lhs = rhs.lhs
		self.rhs = rhs.rhs
		self.op = rhs.op
		self.regex = rhs.regex
		self.name = rhs.name
		self.module = rhs.module
		self.args = rhs.args
		return


	def getValue(self):
		if self.lhs and ((self.opType == UNARY) or (self.opType == NO_OP)):
			return self.lhs
		elif self.rhs and (self.opType == BINARY):
			return self.rhs


	def getNames(self):
		val = self.getValue()
		return val.split(";")


	def printSelf(self):
		str = "ModuleSpec.ModuleInfo: type = %s opType = %s lhs = '%s' rhs = '%s' "
		str = str + "op = '%s' regex = '%s'"
		str = str % (typeToStr(self.type), opTypeToStr(self.opType), self.lhs,
					 self.rhs, self.op, self.regex)
		cairn.debug(str)
		return


def parseModuleSpec(sysdef, moduleSpec, userModuleSpec, prefix):
	modules = splitModuleSpec(moduleSpec, prefix)
	cairn.debug("system module spec:")
	for mod in modules:
		mod.printSelf()
	if userModuleSpec:
		userModuleNames = splitModuleSpec(userModuleSpec, None)
		cairn.debug("user module spec:")
		for mod in userModuleNames:
			mod.printSelf()
		applySpec(modules, userModuleNames)
		cairn.debug("combined spec:")
		for mod in modules:
			mod.printSelf()
	return modules


def splitModuleSpec(moduleSpec, prefix):
	str = moduleSpec.replace(" ", "#")
	str = str.replace("	", "#")
	lexer = shlex.shlex(str, None, True)
	lexer.wordchars = lexer.wordchars + "."
	lexer.commenters = ""
	lexer.whitespace = lexer.whitespace.replace("\n", "")
	lexer.quotes = ""
	parsing = True
	curInfo = None
	nodes = []
	while parsing:
		(token, ttype) = nextToken(lexer)
		if not token:
			break
		if (token == ";"):
			if curInfo:
				if ((curInfo.type == IDENTIFIER) and not curInfo.op and
					curInfo.lhs):
					curInfo.opType = NO_OP
					nodes.append(curInfo)
					curInfo = None
				else:
					raise cairn.Exception("Parse error, unexpected ';'")
		elif (token == "#") or (token == "\n"):
			continue
		elif not curInfo:
			if (ttype == IDENTIFIER) and (token in UNARY_OPS):
				op = token
				(token, ttype) = nextToken(lexer)
				if (ttype == UNKNOWN):
					raise cairn.Exception("Parse error, invalid token '%s' after '%s'" % (token, op))
				if ttype == REGEX:
					curInfo = ModuleInfo(type=IDENTIFIER, opType=UNARY, op=op,
								   lhs=token, regex=True)
				else:
					curInfo = ModuleInfo(type=ttype, opType=UNARY, op=op, lhs=token)
				nodes.append(curInfo)
				curInfo = None
			else:
				if ttype == REGEX:
					curInfo = ModuleInfo(type=IDENTIFIER, lhs=token, regex=True)
				else:
					curInfo = ModuleInfo(type=ttype, lhs=token)
		else:
			if not curInfo.op:
				if ttype != IDENTIFIER:
					raise cairn.Exception("Parse error, expected binary operator")
				if not token in BINARY_OPS:
					raise cairn.Exception("Parse error, invalid binary operator: %s" % token)
				curInfo.op = token
				curInfo.opType = BINARY
			elif curInfo.opType == BINARY:
				if ttype == REGEX:
					raise cairn.Exception("Parse err, found regex '%s' when expected identifier" % token)
				curInfo.rhs = token
				curInfo.type = ttype
				nodes.append(curInfo)
				curInfo = None
	if prefix:
		applyPrefix(nodes, prefix)
	return nodes


def nextToken(lexer):
	token = lexer.get_token()
	if token == "/":
		id = matchToken(lexer, "/")
		if not id:
			raise cairn.Exception("Parse error, invalid regex in module name")
		return (id, REGEX)
	elif token == "(":
		id = matchToken(lexer, "(")
		if not id:
			raise cairn.Exception("Parse error, invalid '()' in module name")
		return (id, USER_MOD_PY)
	elif token == "{":
		id = matchToken(lexer, "{")
		if not id:
			raise cairn.Exception("Parse error, invalid user shell module '{}'")
		return (id, USER_MOD_SHELL)
	elif token == "[":
		id = matchToken(lexer, "[")
		if not id:
			raise cairn.Exception("Parse error, invalid user python module '[]'")
		return (id, USER_MOD_PY)
	else:
		return (token, IDENTIFIER)


def matchToken(lexer, match):
	token = lexer.get_token()
	id = ""
	stack = [match]
	escaped = False
	if match in QUOTES:
		exactMatch = match
	else:
		exactMatch = None
	while token and len(stack):
		if (token == "\\"):
			if escaped:
				escaped = False
			else:
				escaped = True
		elif escaped:
			escaped = False

		if not escaped:
			if token == exactMatch:
				stack.pop()
				exactMatch = None
			elif (not exactMatch) and (token in QUOTES):
				stack.append(token)
				exactMatch = token
			elif (not exactMatch) and (token in ASYM_QUOTES_LHS):
				stack.append(token)
			elif (not exactMatch) and (token in ASYM_QUOTES):
				popped = False
				lhs = QUOTES_GROUPED[token]
				if lhs:
					size = len(stack)
					index = 0
					while size + index >= 0:
						index = index - 1
						if (stack[index + size] == lhs):
							while index < 0:
								stack.pop()
								index = index + 1
							popped = True
							break
					if not popped:
						stack.append(token)
				else:
					stack.append(token)
		if len(stack):
			if token == "#":
				id = id + " "
			else:
				id = id + token
			token = lexer.get_token()
		else:
			break
	if not token:
		return None
	return id


def applyPrefix(nodes, prefix):
	for node in nodes:
		if (node.type == USER_MOD_PY) or (node.type == USER_MOD_SHELL):
			continue
		if node.lhs and ((node.opType == UNARY) or (node.opType == NO_OP)):
			node.lhs = splitApplyPrefix(node.lhs, prefix)
		elif node.rhs and (node.opType == BINARY):
			node.rhs = splitApplyPrefix(node.rhs, prefix)
	return


def splitApplyPrefix(inStr, prefix):
	strs = inStr.split(";")
	outStr = ""
	for str in strs:
		str = str.strip()
		outStr = "%s;%s.%s" % (outStr, prefix, str)
	return outStr.lstrip(";")


def applySpec(moduleNames, userModuleNames):
	for userModule in userModuleNames:
		if (userModule.op == "="):
			applyReplace(moduleNames, userModule)
		elif (userModule.op == "<") or (userModule.op == ">"):
			applyInsert(moduleNames, userModule)
		elif (userModule.op == "-"):
			applyRemove(moduleNames, userModule)
		elif (userModule.op == "^"):
			applyPrepend(moduleNames, userModule)
		elif (userModule.op == "$"):
			applyAppend(moduleNames, userModule)
		elif not userModule.op:
			continue
		else:
			raise cairn.Exception("Unknown operator: %s" % userModule.op)


def makeRE(module):
	if module.regex:
		name = module.lhs
	else:
		name = "^%s$" % module.lhs
	cairn.debug("makeRE: %s" % name)
	return re.compile(name)


def applyReplace(moduleNames, userModule):
	re = makeRE(userModule)
	for i, v in enumerate(moduleNames):
		if re.search(v.getValue()):
			moduleNames[i] = userModule
			break
	return


def applyInsert(moduleNames, userModule):
	if (userModule.op == "<"):
		before = True
	else:
		before = False
	print "insert:", userModule.lhs, userModule.rhs
	re = makeRE(userModule)
	for i, v in enumerate(moduleNames):
		if re.search(v.getValue()):
			print "insert", before
			if before:
				moduleNames.insert(i, userModule)
			else:
				moduleNames.insert(i+1, userModule)
			break
	return


def applyRemove(moduleNames, userModule):
	re = makeRE(userModule)
	for i, v in enumerate(moduleNames):
		if re.search(v.getValue()):
			moduleNames.remove(v)
			break
	return


def applyPrepend(moduleNames, userModule):
	moduleNames.insert(0, userModule)
	return


def applyAppend(moduleNames, userModule):
	moduleNames.append(userModule)
	return


def typeToStr(ttype):
	if ttype == UNKNOWN:
		return "UNKNOWN"
	if ttype == IDENTIFIER:
		return "IDENTIFIER"
	if ttype == USER_MOD_PY:
		return "USER_MOD_PY"
	if ttype == USER_MOD_SHELL:
		return "USER_MOD_SHELL"
	if ttype == MOD_PARAMS:
		return "MOD_PARAMS"
	if ttype == REGEX:
		return "REGEX"
	return "UNDEFINED"


def opTypeToStr(opType):
	if opType == UNARY:
		return "UNARY"
	if opType == BINARY:
		return "BINARY"
	if opType == NO_OP:
		return "NO_OP"
	return "UNDEFINED"
