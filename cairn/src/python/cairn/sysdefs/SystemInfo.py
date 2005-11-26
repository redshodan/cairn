"""System Information -- Collection of the gathered system information

SystemInfo contains all the relavent information about a system broken out
into standardized (at least for this purpose) formats. Some values are
determistic, some are variable strings. If a value is a unformated string
the CAIRN definition will be contained by the variable name. The original
unformated string will be name plus a 'Str' at the end. Here is the list of
used variable names. They are simply strings that need to be passed into
the getValue() function.


Operating System
   <os>
     <name>                  - Base OS name.
     <version>               - Base OS version.
     <version-short>         - Base OS version, shortened to major and minor.
     <version-str>           - Base OS version string
     <distribution-vender>   - OS distribution vendor name.
     <distribution>          - OS distribution name.
     <distribution-version>  - OS distribution version.
   </os>

Architecture
   <arch>
     <name>                - Architecture
	 <cpu>                 - CPU type
     <cpu-str>             - CPU type string
   </arch>

Environment
   <env>
     <path>                - System binary path
     <part-tool>           - Partitioning tool to use
	 <archive-tool>        - Archiving tool to use
   </arch>
"""


from xml.dom import minidom
import string

import cairn


class SystemInfo(object):
	def __init__(self):
		self.createNew()
		self.doc.normalize()
		return


	# Simple string based name/value pair accessors
	def get(self, name):
		elem = self.getElem(name)
		if elem:
			return self.getText(elem)
		return None


	def set(self, name, value):
		elem = self.getElem(name)
		if not elem:
			raise cairn.Exception("In SystemInfo, tag %s was not found" % name)
		self.emptyElem(elem)
		text = self.doc.createTextNode(value)
		elem.appendChild(text)
		return


	# Document handling
	def createNew(self):
		impl = minidom.getDOMImplementation()
		self.doc = impl.createDocument(None, "system-info", None)
		self.root = self.doc.documentElement
		self.createOSElem()
		self.createArchElem()
		self.createEnvElem()
		return


	def createOSElem(self):
		os = self.createElem(self.root, "os")
		elem = self.createElem(os, "name")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "version-short")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "version")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "version-str")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "distribution-vendor")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "distribution")
		self.createText(elem, "unknown")
		elem = self.createElem(os, "distribution-version")
		self.createText(elem, "unknown")
		return os


	def createArchElem(self):
		arch = self.createElem(self.root, "arch")
		elem = self.createElem(arch, "name")
		self.createText(elem, "unknown")
		elem = self.createElem(arch, "cpu")
		self.createText(elem, "unknown")
		elem = self.createElem(arch, "cpu-str")
		self.createText(elem, "unknown")
		return arch


	def createEnvElem(self):
		env = self.createElem(self.root, "env")
		elem = self.createElem(env, "path")
		self.createText(elem, "unknown")
		elem = self.createElem(env, "part-tool")
		self.createText(elem, "unknown")
		elem = self.createElem(env, "archive-tool")
		self.createText(elem, "unknown")
		return env


	def createElem(self, root, name):
		elem = self.doc.createElement(name)
		root.appendChild(elem)
		return elem


	def createText(self, root, name):
		elem = self.doc.createTextNode(name)
		root.appendChild(elem)
		return elem


	def getElem(self, name, root = None):
		if not root:
			root = self.root
		arr = string.split(name, "/")
		elem = root.getElementsByTagName(arr[0])
		if not elem:
			return None
		if len(arr) > 1:
			return self.getElem(arr[1], elem[0])
		if len(elem) == 1:
			return elem[0]
		else:
			return elem
		return


	def getText(self, elem):
		ret = ""
		for child in elem.childNodes:
			if child.nodeType == child.TEXT_NODE:
				ret = ret + child.data
		return ret


	def emptyElem(self, elem):
		while elem.hasChildNodes():
			child = elem.removeChild(elem.firstChild)
			child.unlink()
		return


	def printXML(self):
		print self.doc.toprettyxml("   ")
		return


	def saveToFile(self, file):
		self.doc.writexml(file)
		return


	def printSummary(self):
		print "System Information:"
		print "  OS:       %s, %s, %s" % (self.get("os/name"),
										  self.get("os/version-short"),
										  self.get("os/version"))
		print "  Distro:   %s, %s, %s" % (self.get("os/distribution-vendor"),
										  self.get("os/distribution"),
										  self.get("os/distribution-version"))
		print "  Arch:     %s, %s, %s" % (self.get("arch/name"), self.get("arch/cpu"),
										  self.get("arch/cpu-str"))
		print "  ENV:      path: " + self.get("env/path")
		print "            part: " + self.get("env/part-tool")
		print "            archive: " + self.get("env/archive-tool")
		self.printXML()
		return
