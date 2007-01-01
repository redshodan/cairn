#!/bin/sh

PYTHON=`which python`

if [ -z "${PYTHON}" ]; then
	echo "Error: python version 2.3 or greater is required to run this program"
	exit 1
fi

# mktemp cross platform varies too much. this certainly is not terribly secure,
# but hopefully it wont matter
ALPHA="a b c d e f g h i j k l m n o p q r s t u v w x y z"
for L1 in ${ALPHA}; do
	for L2 in ${ALPHA}; do
		for L3 in ${ALPHA}; do
			if [ ! -f "/tmp/cairn-run-${L1}${L2}${L3}" ]; then break; fi
		done
		if [ ! -f "/tmp/cairn-run-${L1}${L2}${L3}" ]; then break; fi
	done
	if [ ! -f "/tmp/cairn-run-${L1}${L2}${L3}" ]; then break; fi
done
FILE="/tmp/cairn-run-${L1}${L2}${L3}"

cat > ${FILE} <<EOF
import os, os.path, sys, tempfile, atexit

def cleanup():
	if not nocleanup:
		try: os.unlink(srcfile)
		except: pass
		try: os.unlink(libname)
		except: pass
		try: os.rmdir(libdir)
		except: pass

atexit.register(cleanup)

srcfile = os.path.abspath(sys.argv[1])
sys.argv = sys.argv[1:]
cmdname = os.path.abspath(sys.argv[1])
sys.argv = sys.argv[1:]
if "--no-cleanup" in sys.argv:
	nocleanup = True
else:
	nocleanup = False
archive = file(cmdname, "rb")
pos = 0
for line in archive:
	pos = pos + len(line)
	if line.startswith("__ARCHIVE__"):
		break
archive.seek(pos)

libdir = tempfile.mkdtemp("", "cairn-lib-")
libname = os.path.join(libdir, "cairn.lib")
lib = file(libname, "w+b")
line = archive.read(1048576)
while line:
	lib.write(line)
	line = archive.read(1048576)
archive.close()
lib.close()

sys.path.append(libname)

command = "unknown"
if cmdname.endswith("cairn"):
	if (len(sys.argv) >= 2) and (sys.argv[1] == "copy"):
		command = "copy"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "restore"):
		command = "restore"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "extract"):
		command = "extract"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "verify"):
		command = "verify"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "--version"):
		command = "copy"
	elif ((len(sys.argv) >= 2) and
          ((sys.argv[1] == "--help") or (sys.argv[1] == "-h"))):
		command = "help"
elif cmdname.endswith("copy"):
	command = "copy"
elif cmdname.endswith("restore"):
	command = "restore"
elif cmdname.endswith("extract"):
	command = "extract"
elif cmdname.endswith("verify"):
	command = "verify"

if command == "copy":
	from cairn.copy import copy as ccopy
	ccopy.run(libname)
elif command == "restore":
	from cairn.restore import restore
	restore.run(libname)
elif command == "extract":
	from cairn.extract import extract
	extract.run(libname)
elif command == "verify":
	from cairn.verify import verify
	verify.run(libname)
else:
	if command != "help":
		print "Invalid command"
		print
	print "Usage: cairn <command> [command args] ..."
	print "    The command can be one of the following:\n"
	print "    copy  --  Create an image of this computer"
	print "    restore  --  Restore an image to this computer"
	print "    extract  --  Extract files or edit metadata in this image file"
	print "    verify  --  Verify the integrity of this image file\n"
	print "    Place a '--help' after the command to get that commands help."
EOF

python ${FILE} ${FILE} ${0} ${*}

exit ${?}

__ARCHIVE__
