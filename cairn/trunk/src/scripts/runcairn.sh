#!/bin/bash

LIB="/tmp/ccopy.lib"
PWD=`pwd`
BASENAME=`basename $0`
echo $0 | egrep -sq '^/'
if [ $? -eq 0 ]; then
	FILENAME="${PWD}/${BASENAME}"
else
	FILENAME="${PWD}/$0"
fi


ARCHIVE_START=`awk '/^__ARCHIVE__$/ { print NR + 1; exit 0; }' ${FILENAME}`

tail -n +${ARCHIVE_START} ${FILENAME} > ${LIB}
export PYTHONPATH=${LIB}

if [ "$BASENAME" == "ccopy" ]; then
	python -c "from cairn.copy import copy; copy.run();" $*
fi

exit $?

__ARCHIVE__
