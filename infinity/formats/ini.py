# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2008 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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


import re
import sys
from infinity.format import Format, register_format

class INI_Format (Format):
    def __init__ (self):
        Format.__init__ (self)
        #self.expect_signature = 'INI'

        self.ids = {}
        self.ids_re = {}
        self.ids2 = {}
        self.ids2_re = {}
        self.ids_list = []

    def read (self, stream):
        s = ""
        line_no = 0

        while s is not None:
            s = stream.get_line ()
            if s is None:
                break

            line_no = line_no + 1

            s = s.strip ()
            if s == '':
                continue

            if line_no == 1 and (re.match ("^-?[0-9]+$", s) or re.match ("^INI", s)):
                continue

            value = s
            ikey = line_no

            self.ids_list.append ((ikey, value))
            self.ids[ikey] = value

            if self.ids2.has_key (ikey):
                self.ids2[ikey].append (value)
            else:
                self.ids2[ikey] = [ value ]

            self.ids_re[value] = ikey

            if self.ids2_re.has_key (value):
                self.ids2_re[value].append (ikey)
            else:
                self.ids2_re[value] = [ ikey ]

            # FIXME: this is a hack for TRIGGER and ACTION files
            try:
                value2 = value.split ('(', 1)[0]
                self.ids_re[value2] = ikey
            except:
                pass
                

    def key_to_format (self, key):
        if key.startswith ("0x") or key.startswith ("0X"):
            format = key[0:2] + '%0' + str (len (key)-2) + 'X'
        else:
            format = '%d'
        
    def key_to_int (self, key):
        if key.startswith ("0x") or key.startswith ("0X"):
            return int (key[2:], 16)
        else:
            return int (key)

    def printme (self):
        for key, value in self.ids_list:

            print("%s\t%s" %(key, value))
            
    def find (self, key, index=-1):
	if type (key) == type (0):
            if index is None:
                return self.ids2[key]
            else:
                return self.ids2[key][index]
        else:
            if index is None:
                return self.ids2_re[key]
            else:
                return self.ids2_re[key][index]

# FIXME: the signature is bogus
register_format (INI_Format, signature='INI', extension='INI', name='INI', type=0x802)
