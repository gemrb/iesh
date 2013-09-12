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

# Conforms to IESDP 4.2.2009

from infinity.format import Format, register_format
from infinity.stream import MemoryStream


class EFF_V20_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off': 0x0004,
              'label': 'Version'},

            { 'key': 'signature2',
              'type': 'STR4',
              'off': 0x0008,
              'label': 'Signature (on disk)' },

            { 'key': 'version2',
              'type': 'STR4',
              'off': 0x000C,
              'label': 'Version (on disk)'},

            { 'key': 'opcode_number',
              'type': 'DWORD',
              'off': 0x0010,
              'enum': 'effects',
              'label': 'Opcode number'},
            
            { 'key': 'target_type',
              'type': 'DWORD',
              'off': 0x0014,
              'enum': { 0:'None', 1:'Self', 2:'Pre-Target', 3:'Party', 4:'Global', 5:'Non-Party', 6:'Party?', 7:'Unknown1', 8:'Except-Self', 9:'Original-Caster', 10:'Unknown2', 11:'Unknown3', 12:'Unknown4', 13:'Unknown5' }, # check it, done by analogy with SPL.feature_desc
              'label': 'Target type'},
            
            { 'key': 'power',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Power'},
            
            { 'key': 'parameter1',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Parameter 1'},
            
            { 'key': 'parameter2',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Parameter 2'},
            
            { 'key': 'timing_mode',
              'type': 'BYTE',
              'off': 0x0024,
              'enum': { 0x0: 'Duration', 0x1: 'Permanent', 0x2: 'While equipped', 0x3: 'Delayed duration', 0x4: 'Delayed', 0x5: 'Delayed (-> Perm. unsaved)', 0x6: 'Duration?', 0x7: 'Permanent?', 0x8: 'Permanent (unsaved)', 0x9: 'Permanent (after Death)', 0xa: 'Trigger' },
              'label': 'Timing mode'},
            
            { 'key': 'unknown25',
              'type': 'BYTE',
              'off': 0x0025,
              'label': 'Unknown 25'},
            
            { 'key': 'timing',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Timing?'},
            
            { 'key': 'duration',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Duration'},
        
            { 'key': 'probability1',
              'type': 'WORD',
              'off': 0x002C,
              'label': 'Probability 1'},
        
          { 'key': 'probability2',
              'type': 'WORD',
              'off': 0x002E,
              'label': 'Probability 2'},
            
            { 'key': 'resource',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Resref'},
            
            { 'key': 'dice_thrown',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'Dice thrown'},
            
            { 'key': 'dice_sides',
              'type': 'DWORD',
              'off': 0x003C,
              'label': 'Dice sides'},
            
            { 'key': 'saving_throw_type',
              'type': 'DWORD',
              'off': 0x0040,
              'mask': { 0x00: 'None', 0x01: 'Spells', 0x02: 'Breath', 0x04: 'Death', 0x08: 'Wands', 0x10: 'Polymorph' },
              'label': 'Saving throw type'},
            
            { 'key': 'saving_throw_bonus',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Saving throw bonus'},
            
            { 'key': 'variable',
              'type': 'DWORD',
              'off': 0x0048,
              'label': 'Variable?'},
            
            { 'key': 'primary_type',
              'type': 'DWORD',
              'off': 0x004C,
              'label': 'Primary type/School'},
            
            { 'key': 'unknown50',
              'type': 'DWORD',
              'off': 0x0050,
              'label': 'Unknown 50'},
            
            { 'key': 'parent_min_level',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Parent res lowest affected level'},
            
            { 'key': 'parent_max_level',
              'type': 'DWORD',
              'off': 0x0058,
              'label': 'Parent res highest affected level'},
            
            { 'key': 'resistance_type',
              'type': 'DWORD',
              'off': 0x005C,
              'enum': { 0: 'Nonmagical', 1: 'Dispel/Not bypass', 2: 'Not dispel/Not bypass', 3: 'Dispel/Bypass' }, # FIXME: spelling?
              'label': 'Resistance type'},
            
            { 'key': 'parameter3',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Parameter 3'},
            
            { 'key': 'parameter4',
              'type': 'DWORD',
              'off': 0x0064,
              'label': 'Parameter 4'},
            
            { 'key': 'unknown68',
              'type': 'BYTES',
              'off': 0x0068,
              'size': 8,
              'label': 'Unknown 68'},
            
            { 'key': 'parameter5',
              'type': 'RESREF',
              'off': 0x0070,
              'label': 'Parameter 5 (VVC)'},
            
            { 'key': 'unknown78',
              'type': 'DWORD',
              'off': 0x0078,
              'label': 'Unknown 78'},
            
            { 'key': 'unknown7C',
              'type': 'DWORD',
              'off': 0x007C,
              'label': 'Unknown 7C'},
            
            { 'key': 'caster_x_pos',
              'type': 'DWORD',
              'off': 0x0080,
              'label': 'Caster X position'},
            
            { 'key': 'caster_y_pos',
              'type': 'DWORD',
              'off': 0x0084,
              'label': 'Caster Y position'},
            
            { 'key': 'target_x_pos',
              'type': 'DWORD',
              'off': 0x0088,
              'label': 'Target X position'},
            
            { 'key': 'target_y_pos',
              'type': 'DWORD',
              'off': 0x008C,
              'label': 'Target Y position'},
            
            { 'key': 'parent_resource_type',
              'type': 'DWORD',
              'off': 0x0090,
              'enum': { 0: 'None', 1: 'Spell', 2: 'Item' },
              'label': 'Parent resource type'},
            
            { 'key': 'parent_resource',
              'type': 'RESREF',
              'off': 0x0094,
              'label': 'Parent resource'},
            
            { 'key': 'parent_resource_flags',
              'type': 'DWORD',
              'off': 0x009C,
              'label': 'Parent resource flags'}, # FIXME: enum? see IESDP text
            
            { 'key': 'projectile',
              'type': 'DWORD',
              'off': 0x00A0,
              'label': 'Projectile'},
            
            { 'key': 'parent_resource_slot',
              'type': 'DWORD',
              'off': 0x00A4,
              'label': 'Parent resource slot'},
            
            { 'key': 'variable2',
              'type': 'STR32',
              'off': 0x00A8,
              'label': 'Variable 2'},
            
            { 'key': 'caster_level',
              'type': 'DWORD',
              'off': 0x00C8,
              'label': 'Caster level'},
            
            { 'key': 'unknownCC',
              'type': 'DWORD',
              'off': 0x00CC,
              'label': 'Unknown CC'},
            
            { 'key': 'secondary_type',
              'type': 'DWORD',
              'off': 0x00D0,
              'label': 'Secondary type'},
            
            { 'key': 'unknownD4',
              'type': 'DWORD',
              'off': 0x00D4,
              'count': 15,
              'label': 'Unknown D4'},
    )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'EFF'


    def read (self, stream):
        self.read_header (stream)


    def printme (self):
        self.print_header ()

        
register_format (EFF_V20_Format, signature='EFF V2.0')
