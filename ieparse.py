#!/usr/bin/env python

import sys

from infinity import core, stream
from infinity.formats import *

if len (sys.argv) > 1 and sys.argv[1] == '-v':
    core.set_option ('format.mos.print_tiles', True) 
    core.set_option ('format.mos.print_palettes', True)
    core.set_option ('format.tis.print_tiles', True)
    core.set_option ('format.tis.print_palettes', True)
    sys.argv.pop (1)

if len (sys.argv) > 1:
    ffile = sys.argv[1]
else:
    raise ValueError ("missing arg!")


src = stream.FileStream ().open (ffile)
f = src.load_object ()
f.printme ()
