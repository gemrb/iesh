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

# RCS: $Id: tis.py,v 1.1 2006/07/08 14:29:27 edheldil Exp $

from format import Format, register_format, core

class TIS_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'TIS'


        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'count',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Count' },

            { 'key': 'length',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Length' },


            { 'key': 'size',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Size'},

            { 'key': 'offset',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Offset'},

            )


    def decode_file (self):
        self.decode_header ()

    def print_file (self):
        self.print_header ()

    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

        
register_format ('TIS', 'V1  ', TIS_Format)
