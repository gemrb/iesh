# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2009 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

# Conforms to IESDP 22.10.2016

from infinity.format import Format, register_format


class GAM_V11_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature',
              'default': 'GAME' },

            { 'key': 'version',
              'type': 'STR4',
              'off': 0x0004,
              'label': 'Version',
              'default': 'V1.1'},

            { 'key': 'game_time',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Game time (300 units==1 hour)' },

            { 'key': 'formation',
              'type': 'WORD',
              'off': 0x000C,
              'label': 'Selected formation'},

            { 'key': 'formation_button',
              'type': 'WORD',
              'off': 0x000E,
              'count': 5,
              'label': 'Formation button'},

            { 'key': 'gold',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Party gold'},

            { 'key': 'pc_cnt0',
              'type': 'WORD',
              'off': 0x001C,
              'label': 'PC count (excl. protagonist)'},

            { 'key': 'weather',
              'type': 'WORD',
              'off': 0x001E,
              'mask': { 0x01: 'rain', 0x02: 'snow' },
              'label': 'Weather'},

            { 'key': 'pc_off',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'PC offset'},

            { 'key': 'pc_cnt',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'PC count (incl. protagonist)'},

            { 'key': 'unknown28',
              'type': 'DWORD',
              'off': 0x0028,
              'label': '(offset to party inventory)'},

            { 'key': 'unknown2C',
              'type': 'DWORD',
              'off': 0x002C,
              'label': '(count of party inventory)'},

            { 'key': 'npc_off',
              'type': 'DWORD',
              'off': 0x0030,
              'label': 'NPC offset'},

            { 'key': 'npc_cnt',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'NPC count'},

            { 'key': 'global_off',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'GLOBAL variables offset'},

            { 'key': 'global_cnt',
              'type': 'DWORD',
              'off': 0x003C,
              'label': 'GLOBAL variables count'},

            { 'key': 'main_area',
              'type': 'RESREF',
              'off': 0x0040,
              'label': 'Main area'},

            { 'key': 'unknown48',
              'type': 'DWORD',
              'off': 0x0048,
              'label': 'Unknown48'},

            { 'key': 'journal_entry_cnt',
              'type': 'DWORD',
              'off': 0x004C,
              'label': 'Journal entries count'},

            { 'key': 'journal_entry_off',
              'type': 'DWORD',
              'off': 0x0050,
              'label': 'Journal entries offset'},

            { 'key': 'reputation',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Party reputation (*10)'},

            { 'key': 'current_area',
              'type': 'RESREF',
              'off': 0x0058,
              'label': 'Current area'},

            { 'key': 'gui_flags',
              'type': 'DWORD',
              'off': 0x0060,
              'mask': {0x01: 'party_ai_enabled',
                       0x02: 'text_window_size1',
                       0x04: 'text_window_size2',
                       0x08: 'unknown bit3',
                       0x10: 'hide_gui',
                       0x20: 'hide_options',
                       0x40: 'hide_portraits',
                       0x80: 'hide_automap_notes' },
              'label': 'GUI flags'},

            { 'key': 'unknown80',
              'type': 'BYTES',
              'off': 0x0064,
              'size': 80,
              'label': 'Unknown 64'},
    )

    npc_desc = (
            { 'key': 'character_selection',
              'type': 'WORD',
              'off': 0x0000,
              'enum': {0: 'not selected', 1: 'selected', 0x8000: 'dead'},
              'label': 'Character selection'},

            { 'key': 'party_order',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Party order'},

            { 'key': 'cre_off',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'CRE offset'},

            { 'key': 'cre_size',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'CRE size'},

            { 'key': 'character_name',
              'type': 'STR8',
              'off': 0x000C,
              'size': 8,
              'label': 'Character name'},

            { 'key': 'orientation',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Orientation'},

            { 'key': 'current_area',
              'type': 'RESREF',
              'off': 0x0018,
              'label': 'Current area'},

            { 'key': 'x',
              'type': 'WORD',
              'off': 0x0020,
              'label': 'X coordinate'},

            { 'key': 'y',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'Y coordinate'},

            { 'key': 'view_x',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Viewing rectange X coordinate'},

            { 'key': 'view_y',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Viewing rectangle Y coordinate'},

            { 'key': 'modal_action',
              'type': 'WORD',
              'off': 0x0028,
              'label': 'Modal action'},

            { 'key': 'happiness',
              'type': 'WORD',
              'off': 0x002A,
              'label': 'Happiness'},

            { 'key': 'num_times_interacted_npc_count',
              'type': 'DWORD',
              'off': 0x002C,
              'count': 24,
              'label': 'Num times interacted NPC count (unused)' },

            { 'key': 'quick_weapon_slot_index',
              'type': 'WORD',
              'off': 0x008C,
              'count': 4,
              'label': 'Index into slots.ids for Quick Weapon (FFFF=none)' },

            { 'key': 'quick_weapon_slot_ability',
              'type': 'WORD',
              'off': 0x0094,
              'count': 4,
              'label': 'Quick Weapon slot ability (0/1/2 or -1 disabled)' },

            { 'key': 'quick_spell',
              'type': 'RESREF',
              'off': 0x009c,
              'count': 3,
              'label': 'Quick spell' },

            { 'key': 'quick_item_slot_index',
              'type': 'WORD',
              'off': 0x00B4,
              'count': 3,
              'label': 'Index into slots.ids for Quick Item (FFFF=none)' },

            { 'key': 'quick_item_slot_ability',
              'type': 'WORD',
              'off': 0x00BA,
              'count': 3,
              'label': 'Quick Item slot ability (0/1/2 or -1 disabled)' },

            { 'key': 'name',
              'type': 'STR32',
              'off': 0x00C0,
              'label': 'Name' },

            { 'key': 'talkcount',
              'type': 'DWORD',
              'off': 0x00E0,
              'label': 'Talkcount' },

            { 'key': 'stats',
              'type': 'BYTES',
              'off': 0x00E4,
              'size': 116,
              'label': 'Stats' },

            { 'key': 'voiceset',
              'type': 'BYTES',
              'off': 0x0158,
              'size': 8,
              'label': 'Voice set' },

            { 'key': 'voiceset',
              'type': 'STR32',
              'off': 0x0160,
#              'size': 32,
              'label': 'Path to voice set folder (IWD only)' },
    )

    pc_desc = npc_desc

    global_desc = (
            { 'key': 'name',
              'type': 'STR32',
              'off': 0x0000,
              'label': 'Variable name' },

            { 'key': 'unknown20',
              'type': 'BYTES',
              'off': 0x0020,
              'size': 8,
              'label': 'Unknown 20' },

            { 'key': 'value',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Variable value' },

            { 'key': 'unknown2C',
              'type': 'BYTES',
              'off': 0x002C,
              'size': 40,
              'label': 'Unknown 2C' },
    )

    journal_entry_desc = (
            { 'key': 'text',
              'type': 'STRREF',
              'off': 0x0000,
              'label': 'Journal text' },

            { 'key': 'time',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Time (secs)' },

            { 'key': 'current_chapter',
              'type': 'BYTE',
              'off': 0x0008,
              'label': 'Current chapter number' },

            { 'key': 'unknown09',
              'type': 'BYTE',
              'off': 0x0009,
              'label': 'Unknown 09' },

            { 'key': 'section',
              'type': 'BYTE',
              'off': 0x000A,
              'mask': { 0x01: 'quests', 0x02: 'Completed quests', 0x04: 'Journal info' },
              'label': 'Journal section' },

            { 'key': 'location_flag',
              'type': 'BYTE',
              'off': 0x000B,
              'enum': { 0x1F: 'external TOT/TOH', 0xFF: 'internal TLK' },
              'label': 'Location flag' },
    )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'GAME'
        self.pc_list = []
        self.npc_list = []
        self.global_list = []
        self.journal_entry_list = []


    def read (self, stream):
        self.read_header (stream)

        self.read_list (stream, 'pc')
        self.read_list (stream, 'npc')
        self.read_list (stream, 'global')
        self.read_list (stream, 'journal_entry')

    def update (self):
        off = self.size_struc (self.header_desc)
        self.header['pc_cnt'] = len (self.pc_list)
        self.header['pc_off'] = off
        off += self.size_struc (self.pc_desc) * len (self.pc_list)

        pass


    def write (self, stream):
        self.write_header (stream)

        off = self.write_list (stream, off, 'actor')
        raise RuntimeError ("Not implemented")

    def printme (self):
        self.print_header ()

        self.print_list ('pc')
        self.print_list ('npc')
        self.print_list ('global')
        self.print_list ('journal_entry')

        self.print_struc (self.familiar_info, self.familiar_info_desc)


register_format (GAM_V11_Format, signature='GAMEV1.1', extension='GAM', name=('GAM', 'GAME'), type=0x3f5)
