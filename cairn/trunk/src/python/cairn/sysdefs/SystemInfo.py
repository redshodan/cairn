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
     <name/>                  - Base OS name.
     <version/>               - Base OS version.
     <version-short/>         - Base OS version, shortened to major and minor.
     <version-str/>           - Base OS version string
     <distribution-vender/>   - OS distribution vendor name.
     <distribution/>          - OS distribution name.
     <distribution-version/>  - OS distribution version.
   </os>

Architecture
   <arch>
     <name/>                - Architecture
	 <cpu/>                 - CPU type
     <cpu-str/>             - CPU type string
   </arch>

Environment
   <env>
     <path/>                - System binary path
	 <archive-tool>
	 <zip-tool>
	 <tools>
	                        - sysdef dependent tools
     </tools>
   </arch>

Hardware
   <hardware>
     <drive name="">
	   <device/>
	   <os-driver/>
	   <part-tool-cfg/>
	   <partition name="">
	     <device/>
	     <label/>
		 <type/>
		 <fs-type/>
		 <mount/>
		 <space>
		   <total/>
		   <used/>
		   <free/>
		 </space>
	   </partition>
	 </drive>
   </hardware>

Archive
   <archive>
     <filename/>
     <md5sum/>
	 <size/>
	 <offset/>
	 <metafilename/>
     <zip-tool/>
   </archive>

"""


from xml.dom import minidom

import cairn
from cairn import Options


class SystemInfo(object):
	def __init__(self):
		self.createNew()
		self.setOpts(Options.getSysInfoOpts())
		self.doc.normalize()
		return


	# Simple string based name/value pair accessors
	def get(self, name, root = None):
		elem = self.getElem(name, root)
		if elem:
			return self.getText(elem)
		return None


	def getNamed(self, name, instName):
		elems = self.getElems(name)
		if not elems:
			return None
		for elem in elems:
			if elem.getAttribute("name") == instName:
				return elem
		return None


	def getDef(self, name):
		val = self.get(name)
		if not val:
			return "unknown"
		return val


	def set(self, name, value, overridden = False):
		elem = self.getElem(name)
		if not elem:
			elem = self.createElem(self.root, name)
		if elem.getAttribute("overridden"):
			return
		self.setText(elem, value)
		if overridden:
			elem.setAttribute("overridden", "true")
		return


	def setChild(self, root, name, value):
		elem = self.getElem(name, root)
		if not elem:
			elem = self.createElem(root, name)
		self.setText(elem, value)
		return


	def setOpts(self, options):
		for key, val in options.iteritems():
			self.set(key, val, True)
		return


	def isOverriden(self, name):
		elem = self.getElem(name)
		if elem.hasAttribute("overriden"):
			return true
		else:
			return false

	###
	### Document creation
	###
	def createNew(self):
		impl = minidom.getDOMImplementation()
		self.doc = impl.createDocument(None, "cairn-image", None)
		self.root = self.doc.documentElement
		self.createOSElem()
		self.createArchElem()
		self.createEnvElem()
		self.createHardwareElem()
		self.createArchiveElem()
		return


	def createOSElem(self):
		os = self.createElem(self.root, "os")
		elem = self.createElem(os, "name")
		elem = self.createElem(os, "version-short")
		elem = self.createElem(os, "version")
		elem = self.createElem(os, "version-str")
		elem = self.createElem(os, "distribution-vendor")
		elem = self.createElem(os, "distribution")
		elem = self.createElem(os, "distribution-version")
		return os


	def createArchElem(self):
		arch = self.createElem(self.root, "arch")
		elem = self.createElem(arch, "name")
		elem = self.createElem(arch, "cpu")
		elem = self.createElem(arch, "cpu-str")
		return arch


	def createEnvElem(self):
		env = self.createElem(self.root, "env")
		elem = self.createElem(env, "path")
		elem = self.createElem(env, "tools")
		return env


	def createHardwareElem(self):
		return self.createElem(self.root, "hardware")


	def createDriveElem(self, name):
		hardware = self.getElem("hardware")
		drive = self.doc.createElement("drive")
		hardware.appendChild(drive)
		drive.setAttribute("name", name)
		elem = self.createElem(drive, "device")
		elem = self.createElem(drive, "os-driver")
		return drive


	def createPartitionElem(self, drive, name):
		part = self.doc.createElement("partition")
		drive.appendChild(part)
		part.setAttribute("name", name)
		elem = self.createElem(part, "device")
		elem = self.createElem(part, "label")
		elem = self.createElem(part, "type")
		elem = self.createElem(part, "fs-type")
		elem = self.createElem(part, "mount")
		elem = self.createElem(part, "part-tool-cfg")
		return part


	def createPartitionSpaceElem(self, part):
		space = self.doc.createElement("space")
		part.appendChild(space)
		return space


	def createArchiveElem(self):
		archive = self.createElem(self.root, "archive")
		elem = self.createElem(archive, "filename")
		elem = self.createElem(archive, "md5sum")
		elem = self.createElem(archive, "size")
		elem = self.createElem(archive, "offset")
		elem = self.createElem(archive, "metafilename")
		self.setText(elem, "/etc/cairn/cairn-image.xml")
		elem = self.createElem(archive, "zip-tool")
		return archive


	###
	### XML utilities
	###
	def createElem(self, root, name):
		arr = name.split("/")
		elem = self.getLocalElements(root, arr[0])
		if len(arr) > 1:
			if not elem:
				elem = self.doc.createElement(arr[0])
				root.appendChild(elem)
				return self.createElem(elem, "/".join(arr[1:]))
			else:
				return self.createElem(elem[0], "/".join(arr[1:]))
		if len(arr) == 1:
			if elem and elem[0]:
				return elem[0]
			else:
				elem = self.doc.createElement(arr[0])
				root.appendChild(elem)
				return elem
		return


	def setText(self, root, value):
		self.emptyElem(root)
		elem = self.doc.createTextNode(value)
		root.appendChild(elem)
		return elem


	def getElems(self, name, root = None):
		if not root:
			root = self.root
		arr = name.split("/")
		elem = self.getLocalElements(root, arr[0])
		if not elem:
			return []
		if len(arr) > 1:
			return self.getElems("/".join(arr[1:]), elem[0])
		if len(elem) >= 1:
			return elem
		return []


	def getElem(self, name, root = None):
		elems = self.getElems(name, root)
		if len(elems) == 1:
			return elems[0]
		else:
			return elems
		return


	def getLocalElements(self, root, name):
		ret = []
		for elem in root.childNodes:
			if elem.nodeName == name:
				ret.append(elem)
		return ret


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
		print "  OS:       %s, %s, %s" % (self.getDef("os/name"),
										  self.getDef("os/version-short"),
										  self.getDef("os/version"))
		print "  Distro:   %s, %s, %s" % (self.getDef("os/distribution-vendor"),
										  self.getDef("os/distribution"),
										  self.getDef("os/distribution-version"))
		print "  Arch:     %s, %s, %s" % (self.getDef("arch/name"),
										  self.getDef("arch/cpu"),
										  self.getDef("arch/cpu-str"))
		print "  ENV:      path: " + self.getDef("env/path")
		print "            archive-tool: " + self.getDef("env/archive-tool")
		print "            zip-tool: " + self.getDef("env/zip-tool")
		print "            tools: "
		for tool in self.getElem("env/tools").childNodes:
			print "               %s: %s" % (tool.nodeName, self.getText(tool))
		self.printDrives()
		return


	def printDrives(self):
		print "  Drives:"
		for drive in self.getElems("hardware/drive"):
			print "    %s: %s" % (drive.getAttribute("name"),
								  self.get("device", drive))
			for part in self.getElems("partition", drive):
				print "      part %s: device=%s label=%s type=%s fs-type=%s mount=%s" % (part.getAttribute("name"), self.get("device", part), self.get("label", part), self.get("type", part), self.get("fs-type", part), self.get("mount", part)),
				space = self.getElem("space", part)
				if space:
					print " (space: total=%s used=%s free=%s)" % (self.get("total", space), self.get("used", space), self.get("free", space)),
				print
		return
