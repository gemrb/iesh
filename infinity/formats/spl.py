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


from infinity.format import Format, register_format

class SPL_Format (Format):
    header_desc = [
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'spell_name',
              'type': 'STRREF',
              'off': 0x0008,
              'label': 'Spell name'},
            
            { 'key': 'unknown1',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Unknown1'},

            { 'key': 'completion_sound',
              'type': 'RESREF',
              'off': 0x0010,
              'label': 'Completion sound'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Flags'},

            { 'key': 'spell_type',
              'type': 'WORD',
              'off': 0x001C,
              'enum': {0:'Special', 1:'Wizard', 2:'Cleric', 3:'Unknown', 4:'Innate'},
              'label': 'Spell type'},

            { 'key': 'exclusion_school',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'Exclusion school'},

            { 'key': 'priest_type',
              'type': 'WORD',
              'off': 0x0020,
              'mask': {0:'General', 0x4000:'Druid/Ranger', 0x8000:'Cleric/Paladin'},
              'label': 'Priest type'},

            { 'key': 'spell_school',
              'type': 'BYTE',
              'off': 0x0022,
              'label': 'Spell school'},

            { 'key': 'unknown2',
              'type': 'WORD',
              'off': 0x0023,
              'label': 'Unknown2'},

            { 'key': 'primary_type',     # school.ids
              'type': 'WORD',
              'off': 0x0025,
              'label': 'Primary type'},

            { 'key': 'secondary_type',     # secondary.ids
              'type': 'BYTE',
              'off': 0x0027,
              'label': 'Secondary type'},

            { 'key': 'unknown3',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Unknown3'},

            { 'key': 'unknown4',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown4'},

            { 'key': 'unknown5',
              'type': 'DWORD',
              'off': 0x0030,
              'label': 'Unknown5'},

            { 'key': 'spell_level',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Spell level'},

            { 'key': 'unknown6',
              'type': 'WORD',
              'off': 0x0038,
              'label': 'Unknown6'},

            { 'key': 'spellbook_icon',
              'type': 'RESREF',
              'off': 0x003A,
              'label': 'Spellbook icon'},

            { 'key': 'unknown7',
              'type': 'WORD',
              'off': 0x0042,
              'label': 'Unknown7'},

            { 'key': 'unknown8',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Unknown8'},

            { 'key': 'unknown9',
              'type': 'DWORD',
              'off': 0x0048,
              'label': 'Unknown9'},

            { 'key': 'unknown10',
              'type': 'DWORD',
              'off': 0x004C,
              'label': 'Unknown10'},

            { 'key': 'spell_description',
              'type': 'STRREF',
              'off': 0x0050,
              'label': 'Spell description'},

            { 'key': 'unknown11',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Unknown11'},

            { 'key': 'unknown12',
              'type': 'DWORD',
              'off': 0x0058,
              'label': 'Unknown12'},

            { 'key': 'unknown13',
              'type': 'DWORD',
              'off': 0x005C,
              'label': 'Unknown13'},

            { 'key': 'unknown14',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Unknown14'},

            { 'key': 'extended_header_off',
              'type': 'DWORD',
              'off': 0x0064,
              'label': 'Extended header offset'},

            { 'key': 'extended_header_cnt',
              'type': 'WORD',
              'off': 0x0068,
              'label': 'Extended header count'},

            { 'key': 'feature_block_off',
              'type': 'DWORD',
              'off': 0x006A,
              'label': 'Feature block offset'},

            { 'key': 'casting_feature_ndx',
              'type': 'WORD',
              'off': 0x006E,
              'label': 'First casting feature index'},

            { 'key': 'casting_feature_cnt',
              'type': 'WORD',
              'off': 0x0070,
              'label': 'Casting feature count'},

            ]
        
    extended_header_desc = (
            { 'key': 'spell_form',
              'type': 'BYTE',
              'off': 0x0000,
              'label': 'Spell form'},

            { 'key': 'unknown1',
              'type': 'BYTE',
              'off': 0x0001,
              'label': 'Unknown1'},

            { 'key': 'location',
              'type': 'BYTE',
              'off': 0x0002,
              'label': 'Location'},

            { 'key': 'unknown2',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'Unknown2'},

            { 'key': 'memorised_icon',
              'type': 'RESREF',
              'off': 0x0004,
              'label': 'Memorised icon'},

            { 'key': 'target',
              'type': 'BYTE',
              'off': 0x000C,
              'enum': {0:'Invalid', 1:'Creature', 2:'Inventory', 3:'Dead character', 4:'Area', 5:'Self', 6:'Unknown', 7:'None'},
              'label': 'Target'},

            { 'key': 'target_number',
              'type': 'BYTE',
              'off': 0x000D,
              'label': 'Target number'},

            { 'key': 'range',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Range'},

            { 'key': 'level_required',
              'type': 'WORD',
              'off': 0x0010,
              'label': 'Level required'},

            { 'key': 'casting_time',
              'type': 'DWORD',
              'off': 0x0012,
              'label': 'Casting time'},

            { 'key': 'unknown3',
              'type': 'DWORD',
              'off': 0x0016,
              'label': 'Unknown3'},

            { 'key': 'unknown4',
              'type': 'DWORD',
              'off': 0x001A,
              'label': 'Unknown4'},

            { 'key': 'feature_cnt',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'Feature count'},

            { 'key': 'feature_ndx',
              'type': 'WORD',
              'off': 0x0020,
              'label': 'First feature index'},

            { 'key': 'projectile',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'Projectile'},

            { 'key': 'unknown5',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Unknown5'},

            { 'key': 'animation',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Animation'},

            )

    feature_desc = (
            { 'key': 'opcode_number',
              'type': 'WORD',
              'off': 0x0000,
              'enum': 'effects',
              'label': 'Opcode number'},

            { 'key': 'target',
              'type': 'BYTE',
              'off': 0x0002,
              'enum': {0:'None', 1:'Self', 2:'Pre-Target', 3:'Party', 4:'Global', 5:'Non-Party', 6:'Party?', 7:'Unknown1', 8:'Except-Self', 9:'Original-Caster', 10:'Unknown2', 11:'Unknown3', 12:'Unknown4', 13:'Unknown5'},
              'label': 'Target'},

            { 'key': 'power',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'Power'},

            { 'key': 'parameter1',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Parameter1'},

            { 'key': 'parameter2',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Parameter2'},

            { 'key': 'timing_mode',
              'type': 'BYTE',
              'off': 0x000C,
              'enum': {0:'Duration', 1:'Permanent', 2:'While equipped', 3:'Delayed duration', 4:'Delayed2?', 5:'Delayed3?', 6:'Duration2?', 7:'Permanent2?', 8:'Permanent3?', 9:'Permanent? (after Death)', 10:'Trigger'},
              'label': 'Timing mode'},

            { 'key': 'resistance',
              'type': 'BYTE',
              'off': 0x000D,
              'enum': {0:'Nonmagical', 1:'Dispell/Not bypass', 2:'Not dispell/Not bypass', 3:'Dispell/Bypass'},
              'label': 'Resistance'},

            { 'key': 'duration',
              'type': 'DWORD',
              'off': 0x000E,
              'label': 'Duration'},

            { 'key': 'probability1',
              'type': 'BYTE',
              'off': 0x0012,
              'label': 'Probability1'},

            { 'key': 'probability2',
              'type': 'BYTE',
              'off': 0x0013,
              'label': 'Probability2'},

            { 'key': 'resource',
              'type': 'RESREF',
              'off': 0x0014,
              'label': 'Resource'},

            { 'key': 'dice_thrown',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Dice thrown'},

            { 'key': 'dice_sides',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Dice sides'},

            { 'key': 'saving_throw_type',
              'type': 'DWORD',
              'off': 0x0024,
              'mask': {0:'None', 1:'Spells', 2:'Breathe', 4:'Death', 8:'Wands', 16:'Polymorph'},
              'label': 'Saving throw type'},

            { 'key': 'saving_throw_bonus',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Saving throw bonus'},

            { 'key': 'unknown',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown'},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'SPL'

        self.extended_header_list = []
        self.casting_feature_list = []


    def read (self, stream):
        self.read_header (stream)

        off = self.header['extended_header_off']
        for i in range (self.header['extended_header_cnt']):
            obj = {}
            self.read_extended_header (stream, off, obj)
            self.extended_header_list.append (obj)
            off = off + 40

        off = self.header['feature_block_off'] + self.header['casting_feature_ndx'] * 48
        for i in range (self.header['casting_feature_cnt']):
            obj = {}
            self.read_feature_block (stream, off, obj)
            self.casting_feature_block_list.append (obj)
            off = off + 48


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.casting_feature_list:
            print 'Casting feature #%d' %i
            self.print_feature (obj)
            i = i + 1

        i = 0
        for obj in self.extended_header_list:
            print 'Extended header #%d' %i
            self.print_extended_header (obj)
            i = i + 1


    def read_extended_header (self, stream, offset, obj):
        self.read_struc (stream, offset, self.extended_header_desc, obj)

        obj['feature_list'] = []
        off2 = self.header['feature_block_off'] + obj['feature_ndx'] * 48
        for j in range (obj['feature_cnt']):
            obj2 = {}
            self.read_feature (stream, off2, obj2)
            obj['feature_list'].append (obj2)
            off2 = off2 + 48
            
    def print_extended_header (self, obj):
        self.print_struc (obj, self.extended_header_desc)

        j = 0
        for feature in obj['feature_list']:
            print 'Feature #%d' %j
            self.print_feature (feature)
            j = j + 1

    def read_feature (self, stream, offset, obj):
        self.read_struc (stream,offset, self.feature_desc, obj)
        
    def print_feature (self, obj):
        self.print_struc (obj, self.feature_desc)



class SPL_V20_Format (SPL_Format):
    SPL_Format.header_desc.extend ([
            { 'key': 'duration_modifier_level',
              'type': 'BYTE',
              'off': 0x0072,
              'label': 'Duration modifier (level)' },

            { 'key': 'duration_modifier_rounds',
              'type': 'BYTE',
              'off': 0x0073,
              'label': 'Duration modifier (rounds)' }, 

            { 'key': 'unknown_73',
              'type': 'BYTES',
              'off': 0x0074,
              'size': 14, 
              'label': 'Unknown 0x73' },
    ])

    ###Format.get_struc_field (None,  SPL_Format.extended_header_desc, 'off',  0x24)['enum'] = { 0: 'None' }

    def __init__ (self):
        SPL_Format.__init__ (self)


register_format ('SPL', 'V1', SPL_Format,  "Should be done except of enums")
register_format ('SPL', 'V2.0', SPL_V20_Format,  "Should be done except of enums")
