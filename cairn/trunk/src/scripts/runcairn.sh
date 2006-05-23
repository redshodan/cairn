#!/bin/sh

python - $0 $* <<EOF
import os, os.path, sys, tempfile, atexit

def cleanup():
	try: os.unlink(libname)
	except: pass
	try: os.rmdir(libdir)
	except: pass

atexit.register(cleanup)

cmdname = os.path.abspath(sys.argv[1])
sys.argv = sys.argv[1:]
archive = file(cmdname, "rb")
pos = 0
for line in archive:
	pos = pos + len(line)
	if line.startswith("__ARCHIVE__"):
		break
archive.seek(pos)

libdir = tempfile.mkdtemp()
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
	else:
		print "Invalid action"
		print "Usage: %s <action> [action args] ..."
		print "    The action can be 'copy' or 'restore'. Place a '--help' after"
		print "    the action to get that actions help"
elif cmdname.endswith("copy"):
	action = "copy"
elif cmdname.endswith("restore"):
	action = "restore"

if action == "copy":
	from cairn.copy import copy
	copy.run()
elif action == "restore":
	from cairn.restore import restore
	restore.run()
else:
	print "Unable to determine program name."
EOF

exit $?

__ARCHIVE__
