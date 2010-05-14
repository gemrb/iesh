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

# Conforming to IESDP 4.2.2009

from infinity.format import Format, register_format
from infinity.stream import MemoryStream


class CHR_V20_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'name',
              'type': 'STR32',
              'off': 0x0008,
              'label': 'Protagonist/Player name'},

            { 'key': 'cre_off',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'CRE file offset'},

            { 'key': 'cre_len',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'CRE file length'},

            { 'key': 'quick_weapon',
              'type': 'WORD',
              'off': 0x0030,
              'enum': 'SLOTS', 
              'count': 4, 
              'label': 'Quick weapon'},

            { 'key': 'show_quick_weapon',
              'type': 'WORD',
              'off': 0x0038,
              'count': 4, 
              'label': 'Show quick weapon'},

            { 'key': 'quick_spell',
              'type': 'RESREF',
              'off': 0x0040,
              'count': 3, 
              'label': 'Quick spell resref'},

            { 'key': 'quick_item',
              'type': 'WORD',
              'off': 0x0058,
              'enum': 'SLOT',
              'count': 3, 
              'label': 'Quick item'},

            { 'key': 'show_quick_item',
              'type': 'WORD',
              'off': 0x005E,
              'count': 3, 
              'label': 'Show quick item'},
    )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'CHR'

        self.cre = None


    def read (self, stream):
        self.read_header (stream)
        cre = stream.read_blob (self.header['cre_off'],  self.header['cre_len'])
        ms = MemoryStream ().open (cre, 'CRE(@0x%04x in %s)' %(self.header['cre_off'], stream.name))
        self.cre = ms.load_object ()


    def printme (self):
        self.print_header ()
        self.cre.printme ()

        
register_format ('CHR', 'V2.0', CHR_V20_Format)
register_format ('CHR', 'V2.1', CHR_V20_Format)
