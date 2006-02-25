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

DEVICE_RE = [re.compile("hd[a-z]+"), re.compile("sd[a-z]+"),
			 re.compile("ubd[a-z]+")]
