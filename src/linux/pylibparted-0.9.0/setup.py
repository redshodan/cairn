# setup.py - builds pylibparted as a python extension
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

from distutils.core import setup, Extension


setup(name='pylibparted', version='0.9.0',
      author='Ulisses Furquim', author_email='ulissesf@gmail.com',
      url='http://pylibparted.tigris.org/',
      ext_modules=[
      	Extension('pylibparted', ['pylibpartedmodule.c', 'plppeddevice.c',
				  'plppeddisk.c', 'plppeddisktype.c',
				  'plppedgeometry.c', 'plppedfilesystemtype.c',
				  'plppedfilesystem.c', 'plppedpartition.c',
				  'plppedalignment.c', 'plppedconstraint.c',
								  'plppedexception.c', 'plppedtimer.c'],
				  extra_compile_args=['-Wall', '-I../../../build/include'],
				  extra_link_args=['../../../build/lib/libparted.a'],
				  libraries=['dl', 'uuid'])
      ])
