#!/usr/bin/env python

"""Convert Infinity Engine MOS file to TIS file"""

import sys

from infinity import core
from infinity.formats import mos, tis
from infinity import stream

ifile = stream.FileStream ().open (sys.argv[1])
mos_fmt = mos.MOS_Format ().read (ifile)

tis_fmt = tis.TIS_Format ().read (stream.MemoryStream ().open ('TIS V1  ' + 32 * '\0'))
tis_fmt.from_mos (mos_fmt)

ofile = stream.FileStream ().open (sys.argv[2], 'w')
tis_fmt.write (ofile)
