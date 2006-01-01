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

if cmdname.endswith("copy"):
	from cairn.copy import copy
	copy.run()
else:
	print "Unable to determine program name."
EOF

exit $?

__ARCHIVE__
