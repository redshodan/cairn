"""System Information -- Collection of the gathered system information

SystemInfo contains all the relavent information about a system broken out
into standardized (at least for this purpose) formats. Some values are
determistic, some are variable strings. If a value is a unformated string
the CAIRN definition will be contained by the variable name. The original
unformated string will be name plus a 'Str' at the end. Here is the list of
used variable names. They are simply strings that need to be passed into
the getValue() function.


Operating System
   OS                - Base OS name.
   OS_VER            - Base OS version.
   OS_VER_SHORT      - Base OS version, shortened to major and minor.
   OS_VER_STR        - Base OS version string
   OS_DISTRO_VENDOR  - OS distribution vendor name.
   OS_DISTRO         - OS distribution name.
   OS_DISTRO_VER     - OS distribution version.

Architecture
   ARCH              - Architecture
   CPU               - CPU type
   CPU_STR           - CPU type string

Environment
   PATH              - System binary path
   PART_TOOL         - Partitioning tool to use
   ARCHIVE_TOOL      - Archiving tool to use
"""



class SystemInfo(object):
	values = {}


	def __init__(self):
		# Operating System
		self.values["OS"] = "unknown"
		self.values["OS_VER_SHORT"] = "unknown"
		self.values["OS_VER"] = "unknown"
		self.values["OS_DISTRO_VENDOR"] = "unknown"
		self.values["OS_DISTRO"] = "unknown"
		self.values["OS_DISTRO_VER"] = "unknown"

		# Architecture
		self.values["ARCH"] = "unknown"
		self.values["CPU"] = "unknown"
		self.values["CPU_STR"] = "unknown"

		# Environment
		self.values["PATH"] = "unknown"
		self.values["PART_TOOL"] = "unknown"
		self.values["ARCHIVE_TOOL"] = "unknown"


	def get(self, name):
		try:
			return self.values[name]
		except:
			return None


	def set(self, name, value):
		self.values[name] = value


	def printSummary(self):
		print "System Information:"
		print "  OS:       %s, %s, %s" % (self.get("OS"),
										  self.get("OS_VER_SHORT"),
										  self.get("OS_VER"))
		print "  Distro:   %s, %s, %s" % (self.get("OS_DISTRO_VENDOR"),
										  self.get("OS_DISTRO"),
										  self.get("OS_DISTRO_VER"))
		print "  Arch:     %s, %s, %s" % (self.get("ARCH"), self.get("CPU"),
										  self.get("CPU_STR"))
		print "  ENV:      path: " + self.get("PATH")
		print "            part: " + self.get("PART_TOOL")
		print "            archive: " + self.get("ARCHIVE_TOOL")
