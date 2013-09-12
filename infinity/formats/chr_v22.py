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


class CHR_V22_Format (Format):

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

            { 'key': 'quick_weapon1',
              'type': 'WORD',
              'off': 0x0030,
              'label': 'Quick weapon1'},

            { 'key': 'quick_shield1',
              'type': 'WORD',
              'off': 0x0032,
              'label': 'Quick shield1'},

            { 'key': 'quick_weapon2',
              'type': 'WORD',
              'off': 0x0034,
              'label': 'Quick weapon2'},

            { 'key': 'quick_shield2',
              'type': 'WORD',
              'off': 0x0036,
              'label': 'Quick shield2'},

            { 'key': 'quick_weapon3',
              'type': 'WORD',
              'off': 0x0038,
              'label': 'Quick weapon3'},

            { 'key': 'quick_shield3',
              'type': 'WORD',
              'off': 0x003A,
              'label': 'Quick shield3'},

            { 'key': 'quick_weapon4',
              'type': 'WORD',
              'off': 0x003C,
              'label': 'Quick weapon4'},

            { 'key': 'quick_shield4',
              'type': 'WORD',
              'off': 0x003E,
              'label': 'Quick shield4'},

            { 'key': 'quick_weapon_slot_usable',
              'type': 'WORD',
              'off': 0x0040,
              'count': 8,
              'label': 'Quick_weapon slot usable'},

            { 'key': 'quick_spell',
              'type': 'RESREF',
              'off': 0x0050,
              'count': 9,
              'label': 'Quick spell'},

            { 'key': 'quick_spell_class',
              'type': 'BYTE',
              'off': 0x0098,
              'count': 9,
              'label': 'Quick spell class'},
        
            { 'key': 'unknownA1',
              'type': 'BYTE',
              'off': 0x00A1,
              'label': 'Unknown A1'},

            { 'key': 'quick_item',
              'type': 'WORD',
              'off': 0x00A2,
              'count': 3,
              'label': 'Quick item'},

            { 'key': 'quick_item_slot_usable',
              'type': 'WORD',
              'off': 0x00A8,
              'count': 3,
              'label': 'Quick item slot usable'},

            { 'key': 'quick innate',
              'type': 'RESREF',
              'off': 0x00AE,
              'count': 9,
              'label': 'Quick innate'},

            { 'key': 'unknownF6',
              'type': 'DWORD',
              'off': 0x00F6,
              'count': 18,
              'label': 'Unknown F6'},

            { 'key': 'configurable_quickslot',
              'type': 'DWORD',
              'off': 0x013E,
              'count': 9,
              'label': 'Configurable quickslot'},

            { 'key': 'unknown162',
              'type': 'WORD',
              'off': 0x0162,
              'count': 13,
              'label': 'Unknown 162'},

            { 'key': 'soundset',
              'type': 'RESREF',
              'off': 0x017C,
              'label': 'Soundset'},

            { 'key': 'voiceset',
              'type': 'BYTES',
              'off': 0x0184,
              'size': 20,
              'label': 'Voiceset'},

            { 'key': 'unknown1A4',
              'type': 'DWORD',
              'off': 0x01A4,
              'count': 32,
              'label': 'Unknown 1A4'},
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

        
register_format (CHR_V22_Format, signature='CHR V2.2')
