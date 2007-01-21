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

# src file is not piped to python so it does not mess with STDIN and user input
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

#### Command line handling
srcfile = os.path.abspath(sys.argv[0])
sys.argv = sys.argv[1:]
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

python ${FILE} ${0} ${*}

exit ${?}

__ARCHIVE__
