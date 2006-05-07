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

Machine
   <machine>
     <name/>
   </machine>

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
     <excludes>
	   <exclude ignored_fs='T/F:' user='T/F'/>
	 </excludes>
	 <archive-tool/>
	 <archive-tool-cmd/>
     <zip-tool/>
     <zip-tool-cmd/>
   </archive>

"""


from xml.dom import minidom

import cairn
from cairn import Options
from cairn.sysdefs import DOMHelper



PADDING_INT = 25
PADDING_MD5 = 32



def createNew():
	impl = minidom.getDOMImplementation()
	doc = impl.createDocument(None, "cairn-image", None)
	DOMHelper.injectFuncs(doc)
	injectDocFuncs(doc)
	doc.create()
	return doc


###
### Document creation
###

def create(self):
	DOMHelper.injectFuncs(self.documentElement)
	self.createElems()
	self.setOpts(Options.getSysInfoOpts())
	self.normalize()


def setOpts(self, options):
	for key, val in options.iteritems():
		self.setChild(key, val, True)
	return


def createElems(self):
	self.createOSElem()
	self.createArchElem()
	self.createMachineElem()
	self.createEnvElem()
	self.createHardwareElem()
	self.createArchiveElem()
	return


def createOSElem(self):
	os = self.createElem("os")
	elem = os.createElem("name")
	elem = os.createElem("version-short")
	elem = os.createElem("version")
	elem = os.createElem("version-str")
	elem = os.createElem("distribution-vendor")
	elem = os.createElem("distribution")
	elem = os.createElem("distribution-version")
	return os


def createArchElem(self):
	arch = self.createElem("arch")
	elem = arch.createElem("name")
	elem = arch.createElem("cpu")
	elem = arch.createElem("cpu-str")
	return arch


def createMachineElem(self):
	machine = self.createElem("machine")
	elem = machine.createElem("name")


def createEnvElem(self):
	env = self.createElem("env")
	elem = env.createElem("path")
	elem = env.createElem("tools")
	return env


def createHardwareElem(self):
	return self.createElem("hardware")


def createDriveElem(self, name):
	hardware = self.getElem("hardware")
	drive = hardware.createElem("drive=%s" % name)
	elem = drive.createElem("device")
	elem = drive.createElem("os-driver")
	return drive


def createPartitionElem(self, drive, name):
	part = drive.createElem("partition=%s" % name)
	elem = part.createElem("device")
	elem = part.createElem("label")
	elem = part.createElem("type")
	elem = part.createElem("fs-type")
	elem = part.createElem("mount")
	return part


def createPartitionSpaceElem(self, part):
	space = part.createElem("space")
	elem = space.createElem("total")
	elem = space.createElem("used")
	elem = space.createElem("free")
	return space


def createArchiveElem(self):
	archive = self.createElem("archive")
	elem = archive.createElem("filename")
	elem = archive.createPaddedElem("md5sum", PADDING_MD5)
	elem = archive.createPaddedElem("size", PADDING_INT)
	elem = archive.createPaddedElem("shar-offset", PADDING_INT)
	elem = archive.createElem("real-size")
	elem = archive.createElem("adjusted-size")
	elem = archive.createElem("date")
	elem = archive.createElem("metafilename")
	elem = archive.createElem("excludes")
	elem = archive.createElem("excludes-file")
	elem = archive.createElem("user-excludes-file")
	elem = archive.createElem("archive-tool")
	elem = archive.createElem("archive-tool-cmd")
	elem = archive.createElem("zip-tool")
	elem = archive.createElem("zip-tool-cmd")
	elem = archive.createElem("shar", "True")
	return archive


def createArchiveExcludesElem(self, path, type):
	excludes = self.getElem("archive/excludes")
	exclude = excludes.createElem("exclude", path, True)
	exclude.setAttribute("type", type)
	return exclude



###
### SystemInfo Document Functions
###

def printXML(self):
	print self.doc().toprettyxml("   ")
	return


def saveToFile(self, file):
	self.doc().writexml(file, "", "  ", "\n")
	return


def printSummary(self):
	def getDef(info, name):
		val = info.get(name)
		if not val:
			return "unknown"
		return val
	print "System Information:"
	print "  OS:       %s, %s, %s" % (getDef(self, "os/name"),
									  getDef(self, "os/version-short"),
									  getDef(self, "os/version"))
	print "  Distro:   %s, %s, %s" % (getDef(self, "os/distribution-vendor"),
									  getDef(self, "os/distribution"),
									  getDef(self, "os/distribution-version"))
	print "  Arch:     %s, %s, %s" % (getDef(self, "arch/name"),
									  getDef(self, "arch/cpu"),
									  getDef(self, "arch/cpu-str"))
	print "  ENV:      path: " + getDef(self, "env/path")
	print "            archive-tool: " + getDef(self, "env/archive-tool")
	print "            zip-tool: " + getDef(self, "env/zip-tool")
	print "            tools: "
	for tool in self.getElem("env/tools").getElems():
		print "               %s: %s" % (tool.nodeName, tool.getText())
	self.printDrives()
	return


def printDrives(self):
	print "  Drives:"
	for drive in self.getElems("hardware/drive"):
		print "    %s: %s" % (drive.instName(),
							  drive.get("device"))
		for part in drive.getElems("partition"):
			print "      part %s: device=%s label=%s type=%s fs-type=%s mount=%s" % (part.instName(), part.get("device"), part.get("label"), part.get("type"), part.get("fs-type"), part.get("mount")),
			space = part.getElem("space")
			if space:
				print " (space: total=%s used=%s free=%s)" % (space.get("total"), space.get("used"), space.get("free")),
			print
	return


def injectDocFuncs(doc):
	DOMHelper.inject(doc, create)
	DOMHelper.inject(doc, setOpts)
	DOMHelper.inject(doc, createElems)
	DOMHelper.inject(doc, createOSElem)
	DOMHelper.inject(doc, createArchElem)
	DOMHelper.inject(doc, createMachineElem)
	DOMHelper.inject(doc, createEnvElem)
	DOMHelper.inject(doc, createHardwareElem)
	DOMHelper.inject(doc, createDriveElem)
	DOMHelper.inject(doc, createPartitionElem)
	DOMHelper.inject(doc, createPartitionSpaceElem)
	DOMHelper.inject(doc, createArchiveElem)
	DOMHelper.inject(doc, createArchiveExcludesElem)
	DOMHelper.inject(doc, printXML)
	DOMHelper.inject(doc, saveToFile)
	DOMHelper.inject(doc, printSummary)
	DOMHelper.inject(doc, printDrives)
	return
