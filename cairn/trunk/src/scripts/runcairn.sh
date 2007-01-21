#!/bin/sh

PYTHON=`which python`

if [ -z "${PYTHON}" ]; then
	echo "Error: python version 2.3 or greater is required to run this program"
	exit 1
fi

# src file is not piped to python so it does not mess with STDIN and user input
python - ${0} ${*} 4<&0 <<EOF
import os, os.path, sys, tempfile, atexit

def cleanup():
	if not nocleanup:
		try: os.unlink(libname)
		except: pass
		try: os.rmdir(libdir)
		except: pass
	return


def initTemp():
	tmpdir = None
	hit = False
	for arg in sys.argv:
		if arg == "--tmpdir":
			hit = True
		elif hit:
			tmpdir = arg
			break
	if not tmpdir:
		return None
	try:
		info = os.stat(tmpdir)
		if stat.S_ISDIR(info[stat.ST_MODE]):
			return tmpdir
	except:
		pass
	os.makedirs(tmpdir, 0700)
	return tmpdir


#### Start
atexit.register(cleanup)

#### Close up stdin since this script has been read and switch to the tty stdin
os.dup2(4, 0)

#### Command line handling
del sys.argv[0]
cmdname = os.path.abspath(sys.argv[0])
if "--no-cleanup" in sys.argv:
	nocleanup = True
else:
	nocleanup = False
tmpdir = None
if "--tmpdir" in sys.argv:
	tmpdir = initTemp()

#### Open the binary and seek to the start of the python lib
archive = file(cmdname, "rb")
pos = 0
for line in archive:
	pos = pos + len(line)
	if line.startswith("__ARCHIVE__"):
		break
archive.seek(pos)

#### Read the python lib from the binary into a tmp file
libdir = tempfile.mkdtemp("", "cairn-lib-", tmpdir)
libname = os.path.join(libdir, "cairn.lib")
lib = file(libname, "w+b")
line = archive.read(1048576)
while line:
	lib.write(line)
	line = archive.read(1048576)
archive.close()
lib.close()

#### Run it
sys.path.append(libname)

from cairn import cmds
cmds.run(libname)
EOF

exit ${?}

__ARCHIVE__
