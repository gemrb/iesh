#!/usr/bin/env python
# ie_shell.py - Simple shell for Infinity Engine-based game files
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

# RCS: $Id: ie_shell.py,v 1.1 2005/03/02 20:44:21 edheldil Exp $

import atexit
#import os
import os.path
import rlcompleter
import readline
import traceback

from plugins import core
#from plugins.core import *

from formats import *
from plugins import *

###################################################
# Directory where an IE game is installed
#core.game_dir = "/home/benkovsk/dos/iwd2"
core.game_dir = "/home/benkovsk/dos/pst"
#core.game_dir = "/home/benkovsk/dos/bg2"

# Case sensitive names of the central files
core.chitin_file = "CHITIN.KEY"
#core.chitin_file = "Chitin.key"
core.dialog_file = "dialog.tlk"

###################################################
def help_on_shell ():
    print """
    This is a python shell, meaning that the commands you enter
    are python commands and statements (only single-line at the moment).

    Some notable commands:
    
      find_str ("^(?i)gemrb")
          List strrefs for all strings starting with word GemRB, regardless
          of case
          
      export_obj ("GUICG", "GUICG.chu")
          Try to find resource GUICG and export it to file GUICG.chu.
          If the name is not unique, add third parameter,
          e.g. type=0x03ea to restrict the resource type
          
    """


###################################################

# Just enable history and tab completion for the command line
readline.parse_and_bind ("tab: complete")
histfile = os.path.join (os.environ["HOME"], ".ie_shell_history")
try:
    readline.read_history_file (histfile)
except IOError:
    pass

atexit.register (readline.write_history_file, histfile)
del histfile


# Load RESREF index file (CHITIN.KEY)
core.keys = key.KEY_Format (os.path.join (core.game_dir, core.chitin_file))
core.keys.decode_header ()
print "Loading %d file refs and %d RESREFs. This may take ages" %(core.keys.header['num_of_bifs'], core.keys.header['num_of_resrefs'])
core.keys.decode_file ()


# LOAD STRREF index file (DIALOG.TLK)
core.strrefs = tlk.TLK_Format (os.path.join (core.game_dir, core.dialog_file))
core.strrefs.decode_header ()
print "Loading %d STRREFs. This may take eternity" %(core.strrefs.header['num_of_strrefs'])
core.strrefs.decode_file ()



#f = biff.BIFF_Format (os.path.join (game_dir, "Data/Default.bif"))
#f.decode_file ()
#f.print_file ()

#w = wmap.WMAP_Format ("xoxo152")
#w.decode_file ()

#c = chui.CHUI_Format ("GUISAVE.chu")
#c.decode_file ()

print "\nType `help' to print a short help, `quit' or ^D to exit the shell\n"

while 1:
    s = raw_input ('Cmd: ')
    if s == 'q' or s == 'quit':
        break
    if s == '?' or s == 'help':
        help_on_shell ()
        continue
    
    try:
        exec (s)
    except:
        print "\n*** Exception in command ***\n"
        traceback.print_exc ()
        print
        
###################################################
# End of file ie_shell.py
