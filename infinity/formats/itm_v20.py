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

# Conforms to IESDP 4.5.2008

from infinity.format import Format, register_format

class ITM_V20_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'item_name',
              'type': 'STRREF',
              'off': 0x0008,
              'label': 'Item name (generic)'},

            { 'key': 'item_name_identified',
              'type': 'STRREF',
              'off': 0x000C,
              'label': 'Item name (identified)'},

            { 'key': 'replacement_item',
              'type': 'RESREF',
              'off': 0x0010,
              'label': 'Replacement item'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0018,
              'mask': { 0x0001: 'Critical/Unsellable/Kept on ground', 0x0002: 'TwoHanded', 0x0004: 'Movable', 0x0008: 'Displayable', 0x0010: 'Cursed', 0x0020: 'Unknown bit5', 0x0040: 'Magical', 0x0080: 'Bow', 0x0100: 'Silver', 0x0200: 'ColdIron', 0x0400: 'Stolen/Unsellable', 0x0800: 'Uncarriable', 0x1000: 'Pulsating' },
              'label': 'Flags'},

            { 'key': 'item_type',
              'type': 'WORD',
              'off': 0x001C,
              #'enum': {0:''}, # FIXME: define the item types
              'label': 'Item type'},

            { 'key': 'usability_mask',
              'type': 'DWORD',
              'off': 0x001E,
              'mask': {
                       0x00000001: 'Barbarian',
                       0x00000002: 'Bard',
                       0x00000004: 'Cleric',
                       0x00000008: 'Druid',
                       0x00000010: 'Fighter',
                       0x00000020: 'Monk',
                       0x00000040: 'Paladin',
                       0x00000080: 'Ranger',
                       0x00000100: 'Rogue',
                       0x00000200: 'Sorcerer',
                       0x00000400: 'Wizard',
                       0x00000800: 'Unknown bit11',
                       0x00001000: 'Chaotic',
                       0x00002000: 'Evil',
                       0x00004000: 'Good',
                       0x00008000: '...Neutral',
                       0x00010000: 'Lawful',
                       0x00020000: 'Neutral',
                       },
              'label': 'Usability mask'},

            { 'key': 'item_animation',
              'type': 'STR2',
              'off': 0x0022,
              #'enum': {},  # FIXME: IESDP no enum for V2.0?
              'label': 'Item animation'},

            { 'key': 'min_level',
              'type': 'BYTE',
              'off': 0x0024,
              'label': 'Min level'},

            { 'key': 'unknown_25',
              'type': 'BYTE',
              'off': 0x0025,
              'label': 'Unknown 25'},

            { 'key': 'min_str',
              'type': 'BYTE',
              'off': 0x0026,
              'label': 'Min strength'},

            { 'key': 'unknown_27',
              'type': 'BYTE',
              'off': 0x0027,
              'label': 'Unknown 25'},

            { 'key': 'min_str_bonus',
              'type': 'BYTE',
              'off': 0x0028,
              'label': 'Min strength bonus'},

            { 'key': 'unknown_29',
              'type': 'BYTE',
              'off': 0x0029,
              'label': 'Unknown 29'},

            { 'key': 'min_int',
              'type': 'BYTE',
              'off': 0x002A,
              'label': 'Min intelligence'},

            { 'key': 'unknown_2B',
              'type': 'BYTE',
              'off': 0x002B,
              'label': 'Unknown 2B'},

            { 'key': 'min_dex',
              'type': 'BYTE',
              'off': 0x002C,
              'label': 'Min dexterity'},

            { 'key': 'unknown_2D',
              'type': 'BYTE',
              'off': 0x002D,
              'label': 'Unknown 2D'},

            { 'key': 'min_wis',
              'type': 'BYTE',
              'off': 0x002E,
              'label': 'Min wisdom'},

            { 'key': 'unknown_2F',
              'type': 'BYTE',
              'off': 0x002F,
              'label': 'Unknown 2F'},

            { 'key': 'min_con',
              'type': 'BYTE',
              'off': 0x0030,
              'label': 'Min constitution'},

            { 'key': 'weapon_proficiency',
              'type': 'BYTE',
              'off': 0x0031,
              'label': 'Weapon proficiency'},

            { 'key': 'min_cha',
              'type': 'BYTE',
              'off': 0x0032,
              'label': 'Min charisma'},

            { 'key': 'unknown_33',
              'type': 'BYTE',
              'off': 0x0033,
              'label': 'Unknown 33'},

            { 'key': 'price',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Price'},

            { 'key': 'stack_amount',
              'type': 'WORD',
              'off': 0x0038,
              'label': 'Stack amount'},

            { 'key': 'inventory_icon',
              'type': 'RESREF',
              'off': 0x003A,
              'label': 'Inventory icon'},

            { 'key': 'lore_to_id',
              'type': 'WORD',
              'off': 0x0042,
              'label': 'Lore to identify'},

            { 'key': 'ground_icon',
              'type': 'RESREF',
              'off': 0x0044,
              'label': 'Ground icon'},

            { 'key': 'weight',
              'type': 'DWORD',
              'off': 0x004C,
              'label': 'Weight'},

            { 'key': 'item_desc',
              'type': 'STRREF',
              'off': 0x0050,
              'label': 'Item description (generic)'},

            { 'key': 'item_desc_identified',
              'type': 'STRREF',
              'off': 0x0054,
              'label': 'Item description identified'},

            { 'key': 'description_icon',
              'type': 'RESREF',
              'off': 0x0058,
              'label': 'Description icon'},

            { 'key': 'enchantment',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Enchantment'},

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

            { 'key': 'equipping_feature_ndx',
              'type': 'WORD',
              'off': 0x006E,
              'label': 'First equipping feature index'},

            { 'key': 'equipping_feature_cnt',
              'type': 'WORD',
              'off': 0x0070,
              'label': 'Equipping feature count'},

            { 'key': 'unknown_72',
              'type': 'BYTES',
              'off': 0x0072,
              'size': 16,
              'label': 'Unknown 72'},
            )

    extended_header_desc = (
            { 'key': 'attack_type',
              'type': 'BYTE',
              'off': 0x0000,
              'enum': {0: 'None', 1: 'Melee', 2: 'Ranged', 3: 'Magical', 4: 'Launcher'},
              'label': 'Attack type'},

            { 'key': 'id_req',
              'type': 'BYTE',
              'off': 0x0001,
              'mask': { 0x1: 'ID required', 0x2: 'Non-ID required' }, # FIXME: really or just IESDP error?
              'label': 'ID req'},

            { 'key': 'location',
              'type': 'BYTE',
              'off': 0x0002,
              'enum': {0: 'None', 1: 'Weapon', 2: 'Spell', 3: 'Equipment', 4: 'Innate'},
              'label': 'Location'},

            { 'key': 'unknown_03',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'Unknown 03'},

            { 'key': 'use_icon',
              'type': 'RESREF',
              'off': 0x0004,
              'label': 'Use icon'},

            { 'key': 'target',
              'type': 'BYTE',
              'off': 0x000C,
              'enum': { 0:'Invalid', 1:'Creature', 2:'Inventory', 3:'Dead character', 4:'Area', 5:'Self', 6:'Unknown/Crash', 7:'None (Self, ignores pause)' },
              'label': 'Target'},

            { 'key': 'target_cnt',
              'type': 'BYTE',
              'off': 0x000D,
              'label': 'Target count'},

            { 'key': 'range',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Range'},

            { 'key': 'projectile_type',
              'type': 'WORD',
              'off': 0x0010,
              'enum': { 0: 'None', 1: 'Arrow', 2: 'Bolt', 3: 'Bullet' },
              'label': 'Projectile type'},

            { 'key': 'speed',
              'type': 'WORD',
              'off': 0x0012,
              'label': 'Speed'},

            { 'key': 'thac0_bonus',
              'type': 'WORD',
              'off': 0x0014,
              'label': 'THAC0 bonus'},

            { 'key': 'dice_sides',
              'type': 'WORD',
              'off': 0x0016,
              'label': 'Dice sides'},

            { 'key': 'dice_thrown',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'Dice thrown'},

            { 'key': 'damage_bonus',
              'type': 'WORD',
              'off': 0x001A,
              'label': 'Damage bonus'},

            { 'key': 'damage_type',
              'type': 'WORD',
              'off': 0x001C,
              'enum': { 0: 'None', 1: 'Piercing/Magic', 2: 'Blunt', 3: 'Slashing', 4: 'Ranged', 5: 'Fists', 6: 'Piercing/Blunt', 7: 'Piercing/Slashing', 8: 'Blunt/Slashing', 9: 'Blunt missile' },
              'label': 'Damage type'},

            { 'key': 'feature_cnt',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'Feature count'},

            { 'key': 'feature_ndx', # FIXME: IESDP has offset here
              'type': 'WORD',
              'off': 0x0020,
              'label': 'First feature index'},

            { 'key': 'charges',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'Charges'},

            { 'key': 'charges_depletion',
              'type': 'WORD',
              'off': 0x0024,
              'enum': { 0: 'Don\'t vanish', 1: 'Expended', 2: 'Expended (w/o sound)', 3: 'Recharge each day' },
              'label': 'Charges depletion'},

            { 'key': 'flags',
              'type': 'WORD',
              'off': 0x0026,
              'mask': { 0x0001: 'Add strength bonus', 0x0002: 'Breakable', 0x0400: 'Hostile', 0x0800: 'Recharges' },
              'label': 'Flags'},

            { 'key': 'attack_type',
              'type': 'WORD',
              'off': 0x0028,
              'enum': { 0: 'Normal', 1: 'Bypass armor', 2:'Keen' },
              'label': 'Attack type'},

            { 'key': 'projectile_animation',
              'type': 'WORD',
              'off': 0x002A,
              'enum': 'missile', # FIXME: or projectl.ids?
              'label': 'Projectile animation'},

            { 'key': 'melee_animation',
              'type': 'WORD',
              'off': 0x002C,
              'count': 3,
              'label': 'Melee animation'},

            { 'key': 'bow_arrow_qualifier',
              'type': 'WORD',
              'off': 0x0032,
              'label': 'Bow/Arrow qualifier'},

            { 'key': 'crossbow_bolt_qualifier',
              'type': 'WORD',
              'off': 0x0034,
              'label': 'CrossBow/Bolt qualifier'},

            { 'key': 'misc_projectile_qualifier',
              'type': 'WORD',
              'off': 0x0036,
              'label': 'Misc projectile qualifier'},

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
              'enum': { 0:'None', 1:'Self', 2:'Pre-Target', 3:'Party', 4:'Global', 5:'Non-Party', 6:'Non-evil', 7:'Unknown1', 8:'Except-Self', 9:'Original-Caster', 10:'Unknown2', 11:'Unknown3', 12:'Unknown4', 13:'Unknown5' },
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
              'enum': { 0:'Duration', 1:'Permanent', 2:'While equipped', 3:'Delayed duration', 4:'Delayed', 5:'Delayed (chg to 8)', 6:'Duration2?', 7:'Permanent2?', 8:'Permanent (unsaved)', 9:'Permanent (after Death)', 10:'Trigger' },
              'label': 'Timing mode'},

            { 'key': 'resistance',
              'type': 'BYTE',
              'off': 0x000D,
              'enum': { 0:'Nonmagical', 1:'Dispel/Not bypass', 2:'Not dispel/Not bypass', 3:'Dispel/Bypass' },
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
              'type': 'DWORD', # FIXME: IESDP has WORD here
              'off': 0x0020,
              'label': 'Dice sides'},

            { 'key': 'saving_throw_type',
              'type': 'DWORD',
              'off': 0x0024,
              'mask': { 0: 'None', 1:'Spells', 2:'Breathe', 4:'Death', 8:'Wands', 16:'Polymorph'},
              'label': 'Saving throw type' },

            { 'key': 'saving_throw_bonus',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Saving throw bonus'},

            { 'key': 'unknown_2C',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown 2C'},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'ITM'

        self.extended_header_list = []
        self.equipping_feature_list = []


    def read (self, stream):
        self.read_header (stream)
        size_extended = self.get_struc_size (self.extended_header_desc) # 56
        size_feature = self.get_struc_size (self.feature_desc) #48

        off = self.header['extended_header_off']
        for i in range (self.header['extended_header_cnt']):
            obj = {}
            self.read_extended_header (stream, off, obj)
            self.extended_header_list.append (obj)
            off += size_extended

        off = self.header['feature_block_off'] + self.header['equipping_feature_ndx'] * size_feature
        for i in range (self.header['equipping_feature_cnt']):
            obj = {}
            self.read_feature (stream, off, obj)
            self.equipping_feature_list.append (obj)
            off += size_feature

    def write (self, stream):
        size_extended = self.get_struc_size (self.extended_header_desc)
        size_feature = self.get_struc_size (self.feature_desc)

        self.header['extended_header_off'] = self.get_struc_size (self.header)
        self.header['extended_header_cnt'] = len (self.extended_header_list)
        self.header['feature_block_off'] = len (self.extended_header_list) * size_extended
        self.header['equipping_feature_ndx'] = 0
        self.header['equipping_feature_cnt'] = len (self.equipping_feature_list)

        feature_cnt = self.header['equipping_feature_cnt']
        for obj in self.extended_header_list:
            obj['feature_ndx'] = feature_cnt
            obj['feature_cnt'] = len (obj['feature_list'])
            feature_cnt += obj['feature_cnt']

        self.write_header (stream)

        offset = self.header['feature_block_off']
        for obj in self.equipping_feature_list:
            self.write_feature (stream, offset, obj)
            offset += size_feature

        offset = self.header['extended_header_off']
        for obj in self.extended_header_list:
            # FIXME: recalc feature indices
            self.write_extended_header (stream, offset, obj)
            offset += size_extended


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.equipping_feature_list:
            print('Equipping feature #%d' %i)
            self.print_feature (obj)
            i = i + 1

        i = 0
        for obj in self.extended_header_list:
            print('Extended header #%d' %i)
            self.print_extended_header (obj)
            i = i + 1


    def read_extended_header (self, stream, offset, obj):
        self.read_struc (stream, offset, self.extended_header_desc, obj)

        obj['feature_list'] = []
        size_feature = self.get_struc_size (self.feature_desc)
        off2 = self.header['feature_block_off'] + obj['feature_ndx'] * size_feature
        for j in range (obj['feature_cnt']):
            obj2 = {}
            self.read_feature (stream, off2, obj2)
            obj['feature_list'].append (obj2)
            off2 += size_feature

    def write_extended_header (self, stream, offset, obj):
        self.write_struc (stream, offset, obj)
        size_feature = self.get_struc_size (self.feature_desc)
        off2 = self.header['feature_block_off'] +obj['feature_ndx'] * size_feature
        for obj2 in obj['feature_list']:
            self.write_feature (stream, off2, obj2)
            off2 += size_feature

    def print_extended_header (self, obj):
        self.print_struc (obj, self.extended_header_desc)

        j = 0
        for feature in obj['feature_list']:
            print('Feature #%d' %j)
            self.print_feature (feature)
            j = j + 1

    def read_feature (self, stream, offset, obj):
        self.read_struc (stream, offset, self.feature_desc, obj)

    def print_feature (self, obj):
        self.print_struc (obj, self.feature_desc)


register_format (ITM_V20_Format, signature='ITM V2.0')
