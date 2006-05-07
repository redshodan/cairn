"""darwin.unknown.system.Paths system definitions"""


import cairn.sysdefs as sysdefs
import cairn.sysdefs.templates.unix.system.Paths as tmpl
from cairn.sysdefs.Tools import Tool, ToolGroup



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		self.__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
		self.__BINS = [ Tool("fdisk", "env/tools/part", True),
						Tool("disktool", "env/tools/disktool", True),
						Tool("diskutil", "env/tools/diskutil", True),
						ToolGroup("env/archive-tool", "env/archive-tool-user",
								  "archive", True,
								  [ Tool("tar", "env/tools/tar", False),
									Tool("star", "env/tools/star", False) ]),
						ToolGroup("env/zip-tool", "env/zip-tool-user", "zip",
								  True,
								  [ Tool("bzip2", "env/tools/bzip2", False),
									Tool("gzip", "env/tools/gzip", False),
									Tool("compress", "env/tools/compress",
										 False) ])
					  ]
