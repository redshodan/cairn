"""linux.Constants Module"""



import re
import pylibparted as parted



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
	"linux-swap" : "env/tools/mkswap",
	"fat16" : "env/tools/mkfs.msdos",
	"vfat" : "env/tools/mkfs.vfat"
}

FS_LABEL_MAP = {
	"ext2" : "-L",
	"ext3" : "-L",
	"xfs" : "-L",
	"reiserfs" : "-l",
	"jfs" : "-L",
	"fat16" : "-n",
	"vfat" : "-n"
}

PART_TYPE_MAP = \
{
	"extended":parted.PARTITION_EXTENDED, "logical":parted.PARTITION_LOGICAL,
	"lvm":parted.PARTITION_LVM, "metadata":parted.PARTITION_METADATA,
	"primary":parted.PARTITION_NORMAL, "free":parted.PARTITION_FREESPACE
}

FSTAB_UUID_RE = re.compile("\s*UUID=[\-a-fA-F0-9]+\s+/[^\s]*\s+[a-zA-Z0-9]+\s+[=,\-a-zA-Z0-9]+\s+[0-9]+\s+[0-9]+")
FSTAB_LABEL_RE = re.compile("\s*LABEL=[^\s]+\s+/[^\s]*\s+[a-zA-Z0-9]+\s+[=,\-a-zA-Z0-9]+\s+[0-9]+\s+[0-9]+")


MD_RE = [re.compile("md[0-9]+")]
MDP_RE = [re.compile("md_d[0-9]+"), re.compile("mdp[0-9]+")]
LVM_RE = [re.compile("dm[0-9]")]
DRIVE_RE = [re.compile("hd[a-z]+"), re.compile("sd[a-z]+"),
			re.compile("ubd[a-z]+")]
ALL_DEVICE_RE = (MD_RE, MDP_RE, LVM_RE, DRIVE_RE)

### Device types
DEVICE_TYPES = ["drive", "md", "mdp", "lvm"]
DEVICE_MAP = {"drive" : DRIVE_RE, "lvm" : LVM_RE, "md" : MD_RE,
			  "mdp" : MDP_RE}

LVM_COPY_TOOLS = ["pvscan", "vgscan", "lvscan", "vgcfgbackup"]
LVM_RESTORE_TOOLS = ["pvcreate", "vgcfgrestore", "vgchange"]


KERNEL_MODULES = ["dm-mod", "md", "raid0", "raid1", "raid10", "raid5", "raid6",
				  "linear"]
