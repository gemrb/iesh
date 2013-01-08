#!/usr/bin/env python
# mos2tis - Convert Infinity Engine MOS file to TIS file.
# From iesh project, simple shell for Infinity Engine-based game files
# Copyright (C) 2004 by Jaroslav Benkovsky, <edheldil@users.sf.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
Convert Infinity Engine MOS file to TIS file.
Usage:
    mos2tis <MOS File> <TIS File>
"""

import sys

from infinity import core
from infinity.formats import mos, tis
from infinity import stream

if len (sys.argv) != 3:
    print __doc__
    sys.exit (1)

ifile = stream.FileStream ().open (sys.argv[1])
mos_fmt = mos.MOS_Format ().read (ifile)

tis_fmt = tis.TIS_Format ().read (stream.MemoryStream ().open ('TIS V1  ' + 32 * '\0'))
tis_fmt.from_mos (mos_fmt)

ofile = stream.FileStream ().open (sys.argv[2], 'w')
tis_fmt.write (ofile)
ofile.close ()
