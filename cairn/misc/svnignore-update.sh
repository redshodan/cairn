#!/bin/bash


TOP=`pwd`
DIRS=`find . -type d | grep -v .svn`

for DIR in ${DIRS}; do
	cd $TOP
	cd $DIR
	if [ -d .svn ]; then
		svn propset svn:ignore -F ${TOP}/misc/svnignore .
	fi
done
