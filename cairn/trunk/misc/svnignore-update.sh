#!/bin/bash


TOP=`pwd`
DIRS=`find . -type d | grep -v .svn`

for DIR in ${DIRS}; do
	cd $TOP
	cd $DIR
	if [ -d .svn ]; then
		svn propset svn:ignore -F ${TOP}/misc/svnignore .
		echo "	$DIR"
	fi
done
cd ${TOP}

# Adjust a few special cases
if [ -d "${TOP}/misc" ]; then
	cp ${TOP}/misc/svnignore /tmp/svnignore-tmp
	echo build >> /tmp/svnignore-tmp
	svn propset svn:ignore -F /tmp/svnignore-tmp .
	rm /tmp/svnignore-tmp
fi
