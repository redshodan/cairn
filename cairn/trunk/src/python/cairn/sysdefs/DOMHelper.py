"""cairn.sysdefs.DOMHelper Module"""


import new

import cairn.sysdefs.DOMHelper



###
### Accessor functions
###

# Get this nodes text contents, or by path from this node
def get(self, path = None):
	elem = self.root()
	if path:
		elem = self.getElem(path)
	if elem:
		return elem.getText()
	return None


# Get this nodes text contents as an int, or by path from this node.
# Parsing exceptions are possible
def getInt(self, path = None):
	return int(self.getText(path))


# Get this nodes text contents as a long, or by path from this node.
# Parsing exceptions are possible
def getLong(self, path = None):
	return long(self.getText(path))


# Get first child element of this node, or by path from this node
def getElem(self, path = None):
	elems = self.root().getElems(path)
	if len(elems) > 0:
		return elems[0]
	else:
		return None
	return


# Get all child elements of this node, or by path from this node
def getElems(self, path = None):
	found = self.findPath(self.parsePath(path))
	return found.getElems()


# Set value on this node
def set(self, value, overridden = False):
	if self.isOverridden():
		return
	self.setText(value)
	if overridden:
		self.root().setAttribute("overridden", "true")
	return


# Set value on a child of this node
def setChild(self, path, value, overridden = False):
	elem = self.getElem(path)
	if not elem:
		elem = self.createElem(path)
	elem.set(value, overridden)
	return


# Clear value on this node, or by path from this node
def clear(self, path = None):
	elem = self
	if path:
		elem = self.getElem(path)
		if not elem:
			return
	while self.root().hasChildNodes():
		child = self.root().removeChild(self.firstChild)
		child.unlink()
	return


def name(self):
	return self.root().nodeName


def instName(self):
	return self.root().getAttribute("name")



###
### Utilities, not intended for external use
###

class PathEntry(object):
	def __init__(self, name, instName, elem, parent, subPaths):
		self.name = name
		self.instName = instName
		self.elem = elem
		self.parent = parent
		if subPaths:
			self.subPaths = subPaths
		else:
			self.subPaths = []
		return


	def copy(self):
		newEntry = PathEntry(self.name, self.instName, None, None, None)
		if len(self.subPaths) > 0:
			newEntry.subPaths.append(self.subPaths[0].copy())
		return newEntry


	def printMe(self):
		msg = "PathEntry: ("
		if self.elem:
			msg = msg + self.elem + self.elem.instName()
		else:
			msg = msg + self.elem
		msg = msg +  ") %s=%s(%s)" % (self.name, self.instName, self.parent)
		cairn.display(msg)
		for sub in self.subPaths:
			sub.printMe()
		cairn.display("printMe return")
		return


	def getElems(self):
		if not self.subPaths:
			if self.elem:
				return [self.elem]
			else:
				return []
		else:
			elems = []
			for subPath in self.subPaths:
				retElems = subPath.getElems()
				if len(retElems) > 0:
					elems = elems + retElems
			return elems


def parsePath(self, path):
	root = PathEntry(self.name(), self.instName(), self.root(), None, None)
	if path:
		cur = root
		for word in path.split("/"):
			if word.find("=") >= 0:
				arr = word.split("=")
				next = PathEntry(arr[0], arr[1], None, None, None)
			else:
				next = PathEntry(word, None, None, None, None)
			cur.subPaths.append(next)
			next.parent = cur.elem
			cur = next
	return root


# Returns list of selected, parent and remaining path
def findPath(self, path):
	# empty path, return all locals
	if not path:
		ret = []
		for child in self.root().childNodes:
			ret.append(PathEntry(child.name(), child.instName(), child,
								 self.root(), None))
		return ret
	# Find local children that match the path
	newSubPaths = []
	for subPath in path.subPaths:
		subPath.parent = self.root()
		for child in self.root().childNodes:
			if ((child.nodeType == child.ELEMENT_NODE) and
				(child.name() == subPath.name) and
				((subPath.instName and
				  (child.instName() == subPath.instName)) or
				 (not subPath.instName))):
				target = subPath
				# Have a duplicate of the subtree
				if subPath.elem:
					target=subPath.copy()
					newSubPaths.append(target)
				target.elem = child
				if len(target.subPaths) > 0:
					child.findPath(target)
	if len(newSubPaths) > 0:
		path.subPaths = path.subPaths + newSubPaths
	return path


def root(self):
	if self.ownerDocument:
		return self
	else:
		return self.documentElement


def doc(self):
	if self.ownerDocument:
		return self.ownerDocument
	else:
		return self


def isOverridden(self):
	if self.hasAttribute("overridden"):
		return True
	else:
		return False


def createElem(self, path, value = None, multi = False):
	pathArr = self.parsePath(path)
	found = self.findPath(pathArr)
	# Already existing
	elems = found.getElems()
	if (len(elems) > 0) and not multi:
		return elems[0]
	else:
		# create the path all the way to the end
		return self.createPath(found, value, multi)


def createPath(self, path, value, multi):
	if ((not path.elem) or
		((len(path.subPaths) == 0) and multi)):
		elem = self.doc().createElement(path.name)
		path.parent.appendChild(elem)
		cairn.sysdefs.DOMHelper.injectFuncs(elem)
		if path.instName:
			elem.setAttribute("name", path.instName)
		path.elem = elem
		if len(path.subPaths) > 0:
			path.subPaths[0].parent = elem
			return elem.createPath(path.subPaths[0], value, multi)
		else:
			if value:
				elem.setText(value)
			return elem
	elif len(path.subPaths) > 0:
		return path.elem.createPath(path.subPaths[0], value, multi)


# Create a padded size elem big enough to hold any sane sized number
def createPaddedElem(self, name, size):
	elem = self.createElem(name)
	elem.setText("".zfill(size))


def getText(self, path = None):
	elem = self
	if path:
		elem = self.getElem(path)
		if not elem:
			return ""
	ret = ""
	for child in self.childNodes:
		if child.nodeType == child.TEXT_NODE:
			ret = ret + child.data
	return ret.strip()


def setText(self, value):
	self.clear()
	elem = self.doc().createTextNode(value)
	self.root().appendChild(elem)
	return elem


def inject(obj, func):
	setattr(obj, func.__name__, new.instancemethod(func, obj, obj.__class__))
	return


def injectFuncs(elem):
	# Public accessors
	inject(elem, get)
	inject(elem, getInt)
	inject(elem, getLong)
	inject(elem, getElem)
	inject(elem, getElems)
	inject(elem, set)
	inject(elem, setChild)
	inject(elem, clear)
	inject(elem, name)
	inject(elem, instName)

	# semi-private utilities
	inject(elem, parsePath)
	inject(elem, findPath)
	inject(elem, root)
	inject(elem, doc)
	inject(elem, isOverridden)
	inject(elem, createElem)
	inject(elem, createPath)
	inject(elem, createPaddedElem)
	inject(elem, getText)
	inject(elem, setText)
	return


def injectFuncsAllChildren(root):
	injectFuncs(root)
	for child in root.childNodes:
		injectFuncsAllChildren(child)
	return
