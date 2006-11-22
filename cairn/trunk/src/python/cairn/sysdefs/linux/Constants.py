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
	"swap" : "env/tools/mkswap",
}

MD_RE = [re.compile("md[0-9]+")]
MDP_RE = [re.compile("md[0-9]+_d[0-9]+")]
LVM_RE = [re.compile("dm[0-9]")]
DRIVE_RE = [re.compile("hd[a-z]+"), re.compile("sd[a-z]+"),
			re.compile("ubd[a-z]+")]

### Device types
DEVICE_TYPES = ["drive", "md", "mdp", "lvm"]
DEVICE_MAP = {"drive" : DRIVE_RE, "lvm" : LVM_RE, "md" : MD_RE,
			  "mdp" : MDP_RE}

LVM_COPY_TOOLS = ["pvscan", "vgscan", "lvscan", "vgcfgbackup"]
LVM_RESTORE_TOOLS = ["pvcreate", "vgcfgrestore"]
