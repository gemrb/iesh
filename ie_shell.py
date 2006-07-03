#!/usr/bin/env python
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2006 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

# RCS: $Id: ie_shell.py,v 1.5 2006/07/03 18:15:34 edheldil Exp $

import atexit
import os
import os.path
import rlcompleter
import readline
import sys
import traceback

from plugins import core
#from plugins.core import *

from formats import *
from formats.stream import *
from plugins import *

###################################################
## list of commands to be executed before eventual user's input
commands = []

## current indentation for compound commands
indent = ""

## current comound command if non-empty
compound_command = ""

###################################################
def help_on_shell ():
    print """
    This is basically a python shell, meaning that the commands you enter
    are mostly python commands and statements. Compound commands have
    to be terminated by an empty line.

    Use TAB to complete commands, object, attribute or method names, etc.
    Use UP or DOWN cursor keys to navigate in command history
    Use LEFT or RIGHT cursor keys to edit current command
    Use ^R to search in command history

    Some notable commands:
      load_game ("/home/ed/pst", "CHITIN.KEY", "dialog.tlk")
          Loads key and dialog files from the specified directory.
          The directory parameter is mandatory, the others are optional.
          Most of the other commands assume that these two files are
          already loaded. The loaded objects are stored in core.keys and
          core.strrefs.

      load_object ("data/AGOODY.itm")
      load_object ("AGOODY")
          tries to find and load object from a file or resources.
          Returns format object, so the object type has to be supported
    
      find_str ("^(?i)gemrb")
          List strrefs for all strings starting with word GemRB, regardless
          of case
          
      export_obj ("GUICG", "GUICG.chu")
          Try to find resource GUICG and export it to file GUICG.chu.
          If the name is not unique, add third parameter,
          e.g. type=0x03ea to restrict the resource type

      c = chui.CHUI_Format ("GUISAVE.chu")
      c.decode_file ()
      c.print_file ()
           loads file GUISAVE.chu from the current dir, decodes it
           and prints its contents

           key.KEY_Format
           tlk.TLK_Format
           biff.BIFF_Format

           bam.BAM_Format
           chui.CHUI_Format
           cre.CRE_Format   (only parts)
           ids.IDS_Format
           itm.ITM_Format
           spl.SPL_Format   (NOT WORKING!)
           wmap.WMAP_Format

      core.keys.print_bif_record (core.keys.bif_list[0])
      core.strrefs.print_strref_record (core.strrefs.strref_list[0])
           print first records from chitin.key or dialog.tlk file

      !shell_cmd
          Runs command shell_cmd in your native shell. Useful to list
          files on disk, for example.

      quit
          Exit the shell.

    """


###################################################
def read_command_file (filename, add_quit = False):
    try: fh = open (filename)
    except: return False

    commands.extend (map (lambda s: s.rstrip ("\n\r"), fh.readlines ()))

    if add_quit:
        commands.append ("quit")

    return True

###################################################
def read_command (prompt):
    if len (commands) != 0:
        return commands.pop (0)
    else:
        return raw_input (prompt)

###################################################
def readline_init ():
    # Just enable history and tab completion for the command line
    readline.parse_and_bind ("tab: complete")
    histfile = os.path.join (os.environ["HOME"], ".iesh_history")
    try:
        readline.read_history_file (histfile)
    except IOError:
        pass

    atexit.register (readline.write_history_file, histfile)
    del histfile
    readline.set_pre_input_hook (readline_hook)

###################################################
def readline_hook ():
    readline.insert_text (indent)
    readline.redisplay ()


###################################################
###################################################
# main
###################################################

#
# If the program is run with a file parameter, the contents of
# the file are executed and the program quits.
# If it's run without arguments, the program loads and executes
# profile file and starts interactive command prompt
#

if len (sys.argv) > 1:
    res = read_command_file (sys.argv[1], True)
    if not res:
        print "Can't read input file: %s" %sys.argv[1]
        sys.exit (1)
else:
    readline_init ()
    read_command_file (os.path.join (os.environ["HOME"], ".iesh_profile"))
    print "\n\nType `help' to print a short help, `quit' or ^D to exit the shell\n"

#
# Main command processing loop
#

while 1:
    prompt = "Cmd: "
    if compound_command != '':
        prompt = ".... "

    #s = raw_input (prompt)
    s = read_command (prompt)

    indent = s[0:(len (s) - len (s.lstrip ()))]

    if s.endswith (":"):
        indent = indent + "    "

    if (s != '' and compound_command != '') or s.endswith (":"):
        compound_command = compound_command + "\n" + s
        continue

    # zero-length input ends compound commands
    if s == '' and compound_command != '':
        s = compound_command
        compound_command = ''

        
    if s == 'q' or s == 'quit':
        break
        
    if s == '?' or s == 'help':
        help_on_shell ()
        continue
    
    if s.startswith ('!'):
        os.system (s[1:])
        continue

    try:
        exec (s)
    except:
        print "\n*** Exception in command ***\n"
        traceback.print_exc ()
        print


###################################################
# End of file ie_shell.py
