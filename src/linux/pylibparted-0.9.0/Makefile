# Makefile for pylibparted
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

build:
	python setup.py build

install_bin:
	install -d -o root -g root -m 755 ${libdir}/${destdir}/site-packages
	install -o root -g root -m 755 build/lib*/*.so ${libdir}/${destdir}/site-packages

install_doc:
	$(shell 						\
	  cd ${libdir}/${destdir}/site-packages; 		\
	  pydoc -w pylibparted >& /dev/null;			\
	  sed -i -e "s/${buildroot}//g" pylibparted.html;	\
	  mv -f pylibparted.html ${srcdir}/)

install: install_bin install_doc

all: build

clean:
	$(RM) *~
	rm -rf build/
