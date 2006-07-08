# -*-python-*-
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

# RCS: $Id: ids.py,v 1.2 2006/07/08 14:29:26 edheldil Exp $

import re
import sys
from format import Format, register_format

class IDS_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        #self.expect_signature = 'KEY'

        self.ids = {}
        self.ids_re = {}
        self.ids_list = []

    def decode_file (self):
        s = ""
        line_no = 0
        
        while s != None:
            s = self.stream.get_line ()
            if s == None:
                break
            
            line_no = line_no + 1

            s = s.strip ()
            if s == '':
                continue

            if line_no == 1 and (re.match ("^[0-9]+$", s) or re.match ("^IDS", s)):
                continue

            key, value = s.split (None, 1)
            key = key.strip ()
            value = value.strip ()

            if key.startswith ("0x") or key.startswith ("0X"):
                ikey = int (key[2:], 16)
            else:
                ikey = int (key)

            self.ids_list.append ((key, value))

            # FIXME: if keys are duplicate, which one wins?
            #   The first one or the last one?
            if self.ids.has_key (ikey):
                print "Warning: %s: Duplicate key %s" %(self.stream, key)
            else:
                self.ids[ikey] = value

            if self.ids_re.has_key (value):
                print "Warning: %s: Duplicate value %s" %(self.stream, value)
            else:
                self.ids_re[value] = ikey

                

    def print_file (self):
        for key, value in self.ids_list:

            print "%s\t%s" %(key, value)
            


#     def get_bif_by_name_re (self, name):
#         rx = re.compile (name)
#         return filter (lambda s, rx=rx: rx.search (s['file_name']), self.bif_list)


#     def get_resref_by_file_index (self, index):
#         return filter (lambda s, i=index: s['locator_src_ndx'] == i, self.resref_list)

#     def get_resref_by_name_re (self, name):
#         rx = re.compile (name)
#         return filter (lambda s, rx=rx: rx.search (s['resref_name']), self.resref_list)

#     def get_resref_by_name (self, name):
#         return filter (lambda s, name=name: s['resref_name'] == name, self.resref_list)

register_format ('IDS', '', IDS_Format)
