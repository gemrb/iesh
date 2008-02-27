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

# RCS: $Id: itm.py,v 1.1 2005/03/02 20:44:23 edheldil Exp $

from ie_shell.formats.format import Format, register_format

class ITM_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'ITM'

        self.extended_header_list = []
        self.equipping_feature_block_list = []


        self.header_desc = (
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
              'label': 'Item name'},
            
            { 'key': 'item_name_identified',
              'type': 'STRREF',
              'off': 0x000C,
              'label': 'Item Name Identified'},

            { 'key': 'drop_sound',
              'type': 'RESREF',
              'off': 0x0010,
              'label': 'Drop sound'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0018,
              'mask': {0x0001: 'Critical', 0x0002: 'TwoHanded', 0x0004: 'Movable', 0x0008: 'Displayable', 0x0010: 'Cursed', 0x0020: 'NotCopyable', 0x0040: 'Magical', 0x0080: 'Bow', 0x0100: 'Silver', 0x0200: 'ColdIron', 0x0400: 'Stolen', 0x0800: 'Conversable', 0x1000: 'Pulsating'},
              'label': 'Flags'},

            { 'key': 'item_type',
              'type': 'WORD',
              'off': 0x001C,
              'enum': {0:'', 1:''},
              'label': 'Item type'},

            { 'key': 'usability_mask',
              'type': 'DWORD',
              'off': 0x001E,
              'label': 'Usability mask'},

            { 'key': 'inventory_icon_type',
              'type': 'STR2',
              'off': 0x0022,
              'enum': {'  ': 'Fists/Nothing', 'AX': 'Axe', 'DD': 'Dagger', 'CL': 'Club', 'WH': 'Hammer', 'S1': 'Karach', 'CB': 'Crossbow'},
              'label': 'Inventory icon type'},

            { 'key': 'min_level',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Min level'},

            { 'key': 'min_str',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Min strength'},

            { 'key': 'min_str_bonus',
              'type': 'WORD',
              'off': 0x0028,
              'label': 'Min strength bonus'},

            { 'key': 'min_int',
              'type': 'WORD',
              'off': 0x002A,
              'label': 'Min intelligence'},

            { 'key': 'min_dex',
              'type': 'WORD',
              'off': 0x002C,
              'label': 'Min dexterity'},

            { 'key': 'min_wis',
              'type': 'WORD',
              'off': 0x002E,
              'label': 'Min wisdom'},

            { 'key': 'min_con',
              'type': 'WORD',
              'off': 0x0030,
              'label': 'Min constitution'},

            { 'key': 'min_cha',
              'type': 'WORD',
              'off': 0x0032,
              'label': 'Min charisma'},

            { 'key': 'price',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Price'},

            { 'key': 'stack_amount',
              'type': 'WORD',
              'off': 0x0038,
              'label': 'Stack amount'},

            { 'key': 'item_icon',
              'type': 'RESREF',
              'off': 0x003A,
              'label': 'Item icon'},

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
              'label': 'Item description'},

            { 'key': 'item_desc_identified',
              'type': 'STRREF',
              'off': 0x0054,
              'label': 'Item description identified'},

            { 'key': 'pick_up_sound',
              'type': 'RESREF',
              'off': 0x0058,
              'label': 'Pick up sound'},

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

            { 'key': 'equipping_feature_block_off',
              'type': 'WORD',
              'off': 0x006E,
              'label': 'Equipping feature block offset'},

            { 'key': 'equipping_feature_block_cnt',
              'type': 'WORD',
              'off': 0x0070,
              'label': 'Equipping feature block count'},

            # PST only
            { 'key': 'dialog',
              'type': 'RESREF',
              'off': 0x0072,
              'label': 'Dialog'},

            { 'key': 'talking_item_name',
              'type': 'STRREF',
              'off': 0x007A,
              'label': 'Talking item name'},

            { 'key': 'weapon_color',
              'type': 'WORD',
              'off': 0x007E,
              'label': 'Weapon color'},

            )
        
        self.extended_header_desc = (
            { 'key': 'attack_type',
              'type': 'BYTE',
              'off': 0x0000,
              'enum': {0: 'Default', 1: 'Melee', 2: 'Ranged', 3: 'Magical', 4: 'Launcher'},
              'label': 'Attack type'},

            { 'key': 'id_req',
              'type': 'BYTE',
              'off': 0x0001,
              'label': 'ID req'},

            { 'key': 'location',
              'type': 'BYTE',
              'off': 0x0002,
              'enum': {0: 'unknown', 1: 'Weapon slots', 2: 'unknown', 3: 'Item slots', 4: 'Gem?'},
              'label': 'Location'},

            { 'key': 'unknown1',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'Unknown1'},

            { 'key': 'use_icon',
              'type': 'RESREF',
              'off': 0x0004,
              'label': 'Use icon'},

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

            { 'key': 'projectile_type',
              'type': 'WORD',
              'off': 0x0010,
              'enum': {0: 'None', 1: 'Bow', 2: 'Crossbow', 3: 'Sling'},
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
              'enum': {0: 'None', 1: 'Piercing', 2: 'Crushing', 3: 'Slashing', 4: 'Missile', 5: 'Fists'},
              'label': 'Damage type'},

            { 'key': 'feature_cnt',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'Feature count'},

            { 'key': 'feature_off',
              'type': 'WORD',
              'off': 0x0020,
              'label': 'Feature offset'},

            { 'key': 'charges',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'Charges'},

            { 'key': 'charges_depletion',
              'type': 'WORD',
              'off': 0x0024,
              'enum': {0: 'Unknown', 1: 'Item disappears', 2: 'Replace with Used Up', 3: 'Item remains'},
              'label': 'Charges depletion'},

            { 'key': 'use_strength_bonus',
              'type': 'BYTE',
              'off': 0x0026,
              'label': 'Use strength bonus'},

            { 'key': 'recharge',
              'type': 'BYTE',
              'off': 0x0027,
              'enum': {0: 'unknown', 1: 'No', 8: 'After resting'},
              'label': 'Recharge'},

            { 'key': 'unknown2',
              'type': 'WORD',
              'off': 0x0028,
              'label': 'Unknown2'},

            { 'key': 'projectile_animation',
              'type': 'WORD',
              'off': 0x002A,
              'label': 'Projectile animation'},

            { 'key': 'melee_animation_0',
              'type': 'WORD',
              'off': 0x002C,
              'label': 'Melee animation 0'},

            { 'key': 'melee_animation_1',
              'type': 'WORD',
              'off': 0x002E,
              'label': 'Melee animation 1'},

            { 'key': 'melee_animation_2',
              'type': 'WORD',
              'off': 0x0030,
              'label': 'Melee animation 2'},

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

        self.feature_block_desc = (
            { 'key': 'opcode_number',
              'type': 'WORD',
              'off': 0x0000,
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


    def decode_file (self):
        self.decode_header ()

        off = self.header['extended_header_off']
        for i in range (self.header['extended_header_cnt']):
            obj = {}
            self.decode_extended_header (off, obj)
            self.extended_header_list.append (obj)
            off = off + 56

        off = self.header['feature_block_off'] + self.header['equipping_feature_block_off'] * 48
        for i in range (self.header['equipping_feature_block_cnt']):
            obj = {}
            self.decode_feature_block (off, obj)
            self.equipping_feature_block_list.append (obj)
            off = off + 48


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.extended_header_list:
            print '#%d' %i
            self.print_extended_header (obj)
            i = i + 1

        i = 0
        for obj in self.equipping_feature_block_list:
            print '#%d' %i
            self.print_feature_block (obj)
            i = i + 1


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_extended_header (self, offset, obj):
        self.decode_by_desc (offset, self.extended_header_desc, obj)

        obj['feature_list'] = []
        off2 = self.header['feature_block_off'] + obj['feature_off'] * 48
        for j in range (obj['feature_cnt']):
            obj2 = {}
            self.decode_feature_block (off2, obj2)
            obj['feature_list'].append (obj2)
            off2 = off2 + 48
            
    def print_extended_header (self, obj):
        self.print_by_desc (obj, self.extended_header_desc)

        j = 0
        for feature in obj['feature_list']:
            print 'F #%d' %j
            self.print_feature_block (feature)
            j = j + 1

    def decode_feature_block (self, offset, obj):
        self.decode_by_desc (offset, self.feature_block_desc, obj)
        
    def print_feature_block (self, obj):
        self.print_by_desc (obj, self.feature_block_desc)

        
register_format ('ITM', 'V1.1', ITM_Format)
