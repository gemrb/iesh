#!/usr/bin/env python

import sys

from infinity import core, stream
from infinity.formats import *

while len (sys.argv) > 1:
    if sys.argv[1] == '-v':
        core.set_option ('format.print_offset', True) 
        core.set_option ('format.print_size', True) 
        core.set_option ('format.print_type', True) 
        core.set_option ('format.mos.print_tiles', True) 
        core.set_option ('format.mos.print_palettes', True)
        core.set_option ('format.tis.print_tiles', True)
        core.set_option ('format.tis.print_palettes', True)
        sys.argv.pop (1)

    elif sys.argv[1] == '-o':
        sys.argv.pop (1)
        option = sys.argv.pop (1)
        try:
            option, value = option.split ('=')
        except ValueError:
            value = True

        # Convert non-string values
        if value == 'None':
            value = None
        elif value == 'True':
            value = True
        elif value == 'False':
            value = False
        else:
            try: value = int(value)
            except ValueError: pass

        core.set_option (option, value)

    else:
        break


if len (sys.argv) > 1:
    ffile = sys.argv[1]
else:
    print """Usage:
    %s  [-v] [-o option[=value] ] <file>""" %sys.argv[0]
    sys.exit (1)


src = stream.FileStream ().open (ffile)
f = src.load_object ()
f.printme ()
