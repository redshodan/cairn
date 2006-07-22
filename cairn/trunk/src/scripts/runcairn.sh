#!/bin/sh

PYTHON=`which python`

if [ -z "${PYTHON}" ]; then
	echo "Error: python version 2.3 or greater is required to run this program"
	exit 1
fi

# mktemp varies too much. this certainly is not terribly secure, but hopefully
# it wont matter
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
if "--nocleanup" in sys.argv:
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

action = "unknown"
if cmdname.endswith("cairn"):
	if (len(sys.argv) >= 2) and (sys.argv[1] == "copy"):
		action = "copy"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "restore"):
		action = "restore"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "extract"):
		action = "extract"
		sys.argv = sys.argv[1:]
	elif (len(sys.argv) >= 2) and (sys.argv[1] == "--version"):
		action = "copy"
	elif ((len(sys.argv) >= 2) and
          ((sys.argv[1] == "--help") or (sys.argv[1] == "-h"))):
		action = "help"
elif cmdname.endswith("copy"):
	action = "copy"
elif cmdname.endswith("restore"):
	action = "restore"
elif cmdname.endswith("extract"):
	action = "extract"

if action == "copy":
	from cairn.copy import copy
	copy.run(libname)
elif action == "restore":
	from cairn.restore import restore
	restore.run(libname)
elif action == "extract":
	from cairn.extract import extract
	extract.run(libname)
else:
	if action != "help":
		print "Invalid action"
		print
	print "Usage: cairn <action> [action args] ..."
	print "    The action can be 'copy', 'restore' or 'extract'."
	print "    Place a '--help' after the action to get that actions help."
EOF

python ${FILE} ${FILE} ${0} ${*}

exit ${?}

__ARCHIVE__
