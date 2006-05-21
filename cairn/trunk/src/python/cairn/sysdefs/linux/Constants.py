"""linux.Constants Module"""



import re



IGNORED_FS = [
	# Pseudo filesystems
	"proc", "sysfs", "tmpfs", "usbfs", "devpts",

	# Network filesystems
	"nfs", "smbfs", "coda",

	# Misc
	"iso9660"
]

FS_MAP = {
	"ext2" : "env/tools/mkfs.ext2",
	"ext3" : "env/tools/mkfs.ext3",
	"xfs" : "env/tools/mkfs.xfs",
	"jfs" : "env/tools/mkfs.jfs",
	"reiserfs" : "env/tools/mkfs.reiserfs",
}

DEVICE_RE = [re.compile("hd[a-z]+"), re.compile("sd[a-z]+"),
			 re.compile("ubd[a-z]+")]
