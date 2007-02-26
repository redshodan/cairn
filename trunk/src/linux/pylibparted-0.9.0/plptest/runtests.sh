#!/bin/bash

# runtests.sh - run pylibparted test cases
# Copyright (C) 2005 Ulisses Furquim <ulissesf@gmail.com>
#
# This file is part of pylibparted.
#
# pylibparted is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pylibparted is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibparted; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

TESTPROG=./plptest.py
TESTDIR=tests

if [ -d ../build ]; then
    export PYTHONPATH=$(find ../build -maxdepth 1 -mindepth 1 -name 'lib*')
else
    echo ">>>> Warning: did not find a newly compiled pylibparted module"
    echo ">>>>          Trying to use an installed version instead."
fi

for a in $TESTDIR/*.in; do
    echo ">>> Running test $a..."

    if ! $TESTPROG $a; then
	echo ">>>> Error: $TESTPROG exited abnormally"
	exit 1
    fi

    echo ">>> Verifying..."

    device=$(head -n 1 $a | cut -d" " -f2)
    tmpfile=$(mktemp -p /tmp runtests.XXXXXXXXXX)
    base=$TESTDIR/$(basename $a .in)
    out=$base.out

    parted $device print > $tmpfile

    if ! diff -u $tmpfile $out > $base.diff; then
	echo ">>>> Test $a FAILED"
    else
	echo ">>> Ok"
	rm -f $base.diff
    fi

    rm -f $tmpfile
done

exit 0
