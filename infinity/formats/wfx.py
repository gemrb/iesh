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


from infinity import core
from infinity.format import Format, register_format

class WFX_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'unknown_08',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Unknown 08' },

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x000C,
              'mask': { 0x1: 'unknown 0', 0x2: 'unknown 1', 0x4: 'enabled' },
              'label': 'Flags' },


            { 'key': 'deviation',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Deviation'},

            { 'key': 'unknown 14',
              'type': 'BYTES',
              'off': 0x0014,
              'size': 244,
              'label': 'Unknown 14'},

            )


    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'WFX'


    def read (self, stream):
        self.read_header (stream)

    def printme (self):
        self.print_header ()
        

        
register_format ('WFX', 'V1.0', WFX_Format)
