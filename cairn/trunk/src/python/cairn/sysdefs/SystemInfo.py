"""System Information -- Collection of the gathered system information

SystemInfo contains all the relavent information about a system broken out
into standardized (at least for this purpose) formats. Some values are
determistic, some are variable strings. If a value is a unformated string
the CAIRN definition will be contained by the variable name. The original
unformated string will be name plus a 'Str' at the end. Here is the list of
used variable names. They are simply strings that need to be passed into
the getValue() function.


Version
   <version>                  - Version info of the CAIRN that made this image
     <major/>
	 <minor/>
	 <svnrev/>                - SVN revision number for this build
	 <devel/>                 - Is this a devel release.
   </version>

Dates
   <dates>
     <create>date</create>
	 <modify>date</modify>
   </date>

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
	 <bootloader>           - Installed bootloader info
	   <type/>              - Type of installed bootloader
	   <drive/>             - boot drive, bootloader named
	   <drive-os/>          - boot drive, OS named
	   <partition/>         - boot partition, bootloader named
	   <partition-os/>      - boot partition, OS named
	 <bootloader/>
   </machine>

Environment
   <env>
     <path/>                - System binary path
	 <archive-tool/>
	 <zip-tool/>
	 <tools>                - sysdef dependent tools
       <foo/>
     </tools>
   </env>

Hardware
   <hardware>
     <drive-match/>           - perfect, devices, partial or none
     <device name="">
	   <status/>              - probed, skipped, empty
	   <device/>
	   <mapped-device/>
	   <type/>                - drive, md, mdp, lvm
	   <size/>
	   <sector-size/>
       <hw>                   - exists if is a real drive
	     <os-driver/>
	     <model/>
         <bios-geom>
	       <c/> <h/> <s/>
         </bios-geom>
         <hw-geom>
	       <c/> <h/> <s/>
         </hw-geom>
       </hw>
       <disk-label>
         <type/>
         <partition name="">  - exists if is a partitionable device
		   <empty/>
           <device/>
           <mapped-device/>
		   <number/>
           <start/>
           <size/>
           <label/>
           <type/>
           <active/>
           <fs-type/>
           <mount/>
           <flags/>
           <fs-space>
             <total/>
             <used/>
             <free/>
           </fs-space>
         </partition>
       </disk-label>
	   <md-cfg>
	     <md name="">
	       <md-dev/>
		   <level/>
		   <chunk/>
		   <layout/>
		   <device number="" state="">
		 </md>
	   </mdadm-cfg>
     </device>
	 <lvm-cfg>
	   <pvs>
	     <pv vg="" uuid="">
	   </pvs>
	   <vgs>
	     <vg/>
	   </vgs>
	   <lvs>
	     <lv/>
	   </lvs>
	   <vg-backups>
	     <vg name=""/>        - contains the output of vgcfgbackup
       </vg-backups>
	 </lvm-cfg>
   </hardware>

Archive
   <archive>
	 <cmdline/>               - command line used to create the image
     <filename/>
     <md5sum/>
	 <size/>
	 <offset/>
	 <metafilename/>
     <excludes>
	   <exclude ignored_fs='T/F:' user='T/F'/>
	 </excludes>
	 <skip-devices/>
	 <archive-tool/>
	 <archive-tool-cmd/>
     <zip-tool/>
     <zip-tool-cmd/>
   </archive>

Padding
   <pad>000000<pad/>        - Padding to fill out the size of the meta to be 10k
"""


import datetime
from xml.dom import minidom

import cairn
from cairn import Options
from cairn import Version
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


def readNew(aFile):
	doc = minidom.parse(aFile)
	DOMHelper.injectFuncs(doc)
	DOMHelper.injectFuncsAllChildren(doc.root())
	injectDocFuncs(doc)
	doc.unIndent()
	return doc


###
### Document creation
###

def create(self):
	DOMHelper.injectFuncs(self.documentElement)
	self.createElems()
	self.setOpts(Options.getSysInfoOpts())
	self.normalize()
	return


def setOpts(self, options):
	for key, val in options.iteritems():
		self.setChild(key, val, True)
	return


def createElems(self):
	self.createVersionElem()
	self.createDatesElem()
	self.createOSElem()
	self.createArchElem()
	self.createMachineElem()
	self.createEnvElem()
	self.createHardwareElem()
	self.createArchiveElem()
	self.createPadElem()
	return


def createVersionElem(self):
	version = self.createElem("version")
	elem = version.createElem("major", str(Version.MAJOR))
	elem = version.createElem("minor", str(Version.MINOR))
	elem = version.createElem("maint", str(Version.MAINT))
	elem = version.createElem("svnrev", str(Version.SVNREV))
	elem = version.createElem("devel", str(Version.DEVEL))
	return elem


def createDatesElem(self):
	dates = self.createElem("dates")
	return dates


def createDatesDateElem(self, action):
	dates = self.getElem("dates")
	dates.createElem(action, datetime.datetime.now().isoformat(' '), True)
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
	self.createBootloaderElem()
	return machine


def createBootloaderElem(self):
	machine = self.getElem("machine")
	boot = machine.createElem("bootloader")
	elem = boot.createElem("type")
	elem = boot.createElem("drive")
	elem = boot.createElem("drive-os")
	elem = boot.createElem("partition")
	elem = boot.createElem("partition-os")
	return boot


def createEnvElem(self):
	env = self.createElem("env")
	elem = env.createElem("mountdir")
	elem = env.createElem("path")
	elem = env.createElem("tools")
	return env


def createHardwareElem(self):
	hardware = self.createElem("hardware")
	elem = hardware.createElem("drive-match")
	lvm = hardware.createElem("lvm-cfg")
	elem = lvm.createElem("pvs")
	elem = lvm.createElem("vgs")
	elem = lvm.createElem("lvs")
	elem = lvm.createElem("vg-backups")
	return hardware


def createDeviceElem(self, name):
	hardware = self.getElem("hardware")
	device = hardware.createElem("device=%s" % name)
	elem = device.createElem("status")
	elem = device.createElem("device")
	elem = device.createElem("mapped-device")
	elem = device.createElem("type")
	elem = device.createElem("size")
	elem = device.createElem("sector-size")
	return device


def createDeviceHWElem(self, device):
	hw = device.createElem("hw")
	elem = hw.createElem("os-driver")
	elem = hw.createElem("model")
	return hw


def createDeviceHWGeomElem(self, hw, name, c, h, s):
	geom = hw.createElem(name)
	elem = geom.createElem("c", c)
	elem = geom.createElem("h", h)
	elem = geom.createElem("s", s)
	return geom


def createDiskLabelElem(self, device):
	dlabel = device.createElem("disk-label")
	elem = dlabel.createElem("type")
	return dlabel


def createDeviceMDConfigElem(self, device):
	mdcfg = device.createElem("md-cfg")
	elem = mdcfg.createElem("md-dev")
	elem = mdcfg.createElem("level")
	elem = mdcfg.createElem("chunk")
	elem = mdcfg.createElem("layout")
	return mdcfg


def createDeviceMDDeviceElem(self, mdcfg, name, state):
	device = mdcfg.createElem("device", name, True)
	device.setAttribute("state", state)
	return device


def createPartitionElem(self, device, name):
	dlabel = device.getElem("disk-label")
	part = dlabel.createElem("partition=%s" % name)
	elem = part.createElem("status")
	elem = part.createElem("device")
	elem = part.createElem("mapped-device")
	elem = part.createElem("number")
	elem = part.createElem("start")
	elem = part.createElem("size")
	elem = part.createElem("label")
	elem = part.createElem("type")
	elem = part.createElem("active")
	elem = part.createElem("fs-type")
	elem = part.createElem("mount")
	elem = part.createElem("flags")
	return part


def createPartitionFSSpaceElem(self, part):
	space = part.createElem("fs-space")
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


def createPadElem(self):
	return self.createElem("pad")


###
### SystemInfo Document Functions
###

def setPad(self):
	xml = self.doc().toxml()
	length = len(xml)
	if length > 10240:
		cairn.debug("XML is %d long. Not padding." % length)
		return
	# size adjust 6 for '<pad>' plus a '\n'. '</pad>' is already in xml as
	# an empty element.
	padlen = 10240 - length - 6
	cairn.debug("Padding XML by %d." % padlen)
	pad =  "".zfill(padlen)
	pad = pad.replace("0", "*")
	self.setChild("pad", pad)
	return


def verify(self):
	error = False
	if not self.get("cairn-image"): error = True
	if not self.get("version"): error = True
	if not self.get("dates"): error = True
	if not self.get("os"): error = True
	if not self.get("arch"): error = True
	if not self.get("machine"): error = True
	if not self.get("env"): error = True
	if not self.get("hardware"): error = True
	if not self.get("archive"): error = True
	if not self.get("pad"): error = True
	return error


def printXML(self):
	cairn.display(self.doc().toprettyxml("   "))
	return


def saveToFile(self, file, pretty):
	if pretty:
		file.write(self.prettyStr())
	else:
		self.unIndent()
		self.setPad()
		file.write(self.doc().toxml())
	return


def prettyStr(self):
	self.clear("pad")
	return self.root().toPrettyStr()


def printSummary(self):
	def getDef(info, name):
		val = info.get(name)
		if not val:
			return "unknown"
		return val
	cairn.display("System Information:")
	cairn.display("  OS:       %s, %s, %s" % (getDef(self, "os/name"),
											  getDef(self, "os/version-short"),
											  getDef(self, "os/version")))
	cairn.display("  Distro:   %s, %s, %s" %
				  (getDef(self, "os/distribution-vendor"),
				   getDef(self, "os/distribution"),
				   getDef(self, "os/distribution-version")))
	cairn.display("  Arch:     %s, %s, %s" % (getDef(self, "arch/name"),
											  getDef(self, "arch/cpu"),
											  getDef(self, "arch/cpu-str")))
	cairn.display("  ENV:      path: " + getDef(self, "env/path"))
	cairn.display("            archive-tool: " +
				  getDef(self, "env/archive-tool"))
	cairn.display("            zip-tool: " + getDef(self, "env/zip-tool"))
	cairn.display("            tools: ")
	for tool in self.getElem("env/tools").getElems():
		cairn.display("               %s: %s" % (tool.nodeName, tool.getText()))
	self.printDevices()
	return


def printDevices(self):
	cairn.display("  Devices:")
	for device in self.getElems("hardware/device"):
		cairn.display("    %s: %s" % (device.instName(), device.get("device")))
		if device.get("status") == "empty":
			cairn.display("      empty")
		elif device.get("status") == "skipped":
			cairn.display("      skipped")
		for part in device.getElems("disk-label/partition"):
			msg = "      part %s: device=%s label=%s type=%s fs-type=%s mount=%s" % (part.instName(), part.get("device"), part.get("label"), part.get("type"), part.get("fs-type"), part.get("mount"))
			space = part.getElem("fs-space")
			if space:
				msg = msg + " (fs-space: total=%s used=%s free=%s)" % (space.get("total"), space.get("used"), space.get("free"))
			cairn.display(msg)
	return


###
### Parsing accessors
###

def getSkipDevices(self):
	skip = self.get("archive/skip-devices")
	skips = []
	if skip:
		for word in skip.split(","):
			dev = words.lstrip("/dev/")
			skips.append(word)
	return skips


def getDeviceMap(self):
	devmap = {}
	for device in self.getElems("hardware/device"):
		if ((device.get("status") == "probed") and
			(device.get("type") == "drive")):
			devmap[device.get("device")] = device.get("mapped-device")
	return devmap


def mapDevice(self, devmap, str):
	for dev in devmap.keys():
		str = str.replace(dev, devmap[dev])
	return str


def injectDocFuncs(doc):
	DOMHelper.inject(doc, create)
	DOMHelper.inject(doc, setOpts)
	DOMHelper.inject(doc, createElems)
	DOMHelper.inject(doc, createVersionElem)
	DOMHelper.inject(doc, createDatesElem)
	DOMHelper.inject(doc, createDatesDateElem)
	DOMHelper.inject(doc, createOSElem)
	DOMHelper.inject(doc, createArchElem)
	DOMHelper.inject(doc, createMachineElem)
	DOMHelper.inject(doc, createBootloaderElem)
	DOMHelper.inject(doc, createEnvElem)
	DOMHelper.inject(doc, createHardwareElem)
	DOMHelper.inject(doc, createDeviceElem)
	DOMHelper.inject(doc, createDeviceHWElem)
	DOMHelper.inject(doc, createDeviceHWGeomElem)
	DOMHelper.inject(doc, createDiskLabelElem)
	DOMHelper.inject(doc, createDeviceMDConfigElem)
	DOMHelper.inject(doc, createDeviceMDDeviceElem)
	DOMHelper.inject(doc, createPartitionElem)
	DOMHelper.inject(doc, createPartitionFSSpaceElem)
	DOMHelper.inject(doc, createArchiveElem)
	DOMHelper.inject(doc, createArchiveExcludesElem)
	DOMHelper.inject(doc, createPadElem)
	DOMHelper.inject(doc, setPad)
	DOMHelper.inject(doc, verify)
	DOMHelper.inject(doc, printXML)
	DOMHelper.inject(doc, saveToFile)
	DOMHelper.inject(doc, prettyStr)
	DOMHelper.inject(doc, printSummary)
	DOMHelper.inject(doc, printDevices)
	DOMHelper.inject(doc, getSkipDevices)
	DOMHelper.inject(doc, getDeviceMap)
	DOMHelper.inject(doc, mapDevice)
	return
