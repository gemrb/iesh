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

class ITM_V10_Format (Format):
    kit_usability_mask_1 = {
            0x00000001: 'Cleric of Talos',
            0x00000002: 'Cleric of Helm',
            0x00000004: 'Cleric of Lathlander',
            0x00000008: 'Totemic Druid',
            0x00000010: 'Shapeshifter Druid',
            0x00000020: 'Avenger Druid',
            0x00000040: 'Barbarian',
            0x00000080: 'Wildmage',
            }

    kit_usability_mask_2 = {
            0x00000001: 'Stalker Ranger',
            0x00000002: 'Beastmaster Ranger',
            0x00000004: 'Assassin Thief',
            0x00000008: 'Bounty hunter Thief',
            0x00000010: 'Swashbuckler Thief',
            0x00000020: 'Blade Bard',
            0x00000040: 'Jester Bard',
            0x00000080: 'Skald Bard',
            }

    kit_usability_mask_3 = {
            0x00000001: 'Diviner',
            0x00000002: 'Enchanter',
            0x00000004: 'Illusionist',
            0x00000008: 'Invoker',
            0x00000010: 'Necromancer',
            0x00000020: 'Transmuter',
            0x00000040: 'Generalist',
            0x00000080: 'Archer',
            }

    kit_usability_mask_4 = {
            0x00000001: 'Berserker Fighter',
            0x00000002: 'Wizardslayer Fighter',
            0x00000004: 'Kensai Fighter',
            0x00000008: 'Cavalier Paladin',
            0x00000010: 'Inquisitor Paladin',
            0x00000020: 'Undead hunter Paladin',
            0x00000040: 'Abjurer',
            0x00000080: 'Conjurer',
            }

    item_types = {
            0x0000: 'Books/misc',
            0x0001: 'Amulets and necklaces',
            0x0002: 'Armor',
            0x0003: 'Belts and girdles',
            0x0004: 'Boots',
            0x0005: 'Arrows',
            0x0006: 'Bracers and gauntlets',
            0x0007: 'Helms, hats, and other head-wear',
            0x0008: 'Keys (not in Icewind Dale?)',
            0x0009: 'Potions',
            0x000a: 'Rings',
            0x000b: 'Scrolls',
            0x000c: 'Shields (not in IWD)',
            0x000d: 'Food',
            0x000e: 'Bullets (for a sling)',
            0x000f: 'Bows',
            0x0010: 'Daggers',
            0x0011: 'Maces (in BG, this includes clubs)',
            0x0012: 'Slings',
            0x0013: 'Small swords',
            0x0014: 'Large swords',
            0x0015: 'Hammers',
            0x0016: 'Morning stars',
            0x0017: 'Flails',
            0x0018: 'Darts',
            0x0019: 'Axes',
            0x001a: 'Quarterstaff',
            0x001b: 'Crossbow',
            0x001c: 'Hand-to-hand weapons (fist, fist irons, punch daggers, etc)',
            0x001d: 'Spears',
            0x001e: 'Halberds (2-handed polearms)',
            0x001f: 'Crossbow bolts',
            0x0020: 'Cloaks and robes',
            0x0021: 'Gold pieces',
            0x0022: 'Gems',
            0x0023: 'Wands',
            0x0024: 'Container/eye/broken armor',
            0x0025: 'Books/Broken shield/bracelet',
            0x0026: 'Familiars/Broken sword/earring',
            0x0027: 'Tattoos (PST)',
            0x0028: 'Lenses (PST)',
            0x0029: 'Buckler/teeth',
            0x002a: 'Candle',
            0x002b: 'Unknown',
            0x002c: 'Clubs (IWD)',
            0x002d: 'Unknown',
            0x002e: 'Unknown',
            0x002f: 'Large Shield (IWD)',
            0x0030: 'Unknown',
            0x0031: 'Medium Shield (IWD)',
            0x0032: 'Notes',
            0x0033: 'Unknown',
            0x0034: 'Unknown',
            0x0035: 'Small Shield (IWD)',
            0x0036: 'Unknown',
            0x0037: 'Telescope (IWD)',
            0x0038: 'Drink (IWD)',
            0x0039: 'Great Sword (IWD)',
            0x003a: 'Container',
            0x003b: 'Fur/pelt',
            0x003c: 'Leather Armor',
            0x003d: 'Studded Leather Armor',
            0x003e: 'Chain Mail',
            0x003f: 'Splint Mail',
            0x0040: 'Half Plate',
            0x0041: 'Full Plate',
            0x0042: 'Hide Armor',
            0x0043: 'Robe',
            0x0044: 'Unknown',
            0x0045: 'Bastard Sword',
            0x0046: 'Scarf',
            0x0047: 'Food (IWD2)',
            0x0048: 'Hat',
            0x0049: 'Gauntlet'
            }

    weapon_proficiencies = {
            0x000: 'None',
            0x059: 'Bastard Sword',
            0x05A: 'Long Sword',
            0x05B: 'Short Sword',
            0x05C: 'Axe',
            0x05D: 'Two-Handed Sword',
            0x05E: 'Katana',
            0x05F: 'Scimitar/Wakizashi/Ninja-To',
            0x060: 'Dagger',
            0x061: 'War Hammer',
            0x062: 'Spear',
            0x063: 'Halberd',
            0x064: 'Flail/Morningstar',
            0x065: 'Mace',
            0x066: 'Quarterstaff',
            0x067: 'Crossbow',
            0x068: 'Long Bow',
            0x069: 'Short Bow',
            0x06A: 'Darts',
            0x06B: 'Sling',
            0x06C: 'Blackjack',
            0x06D: 'Gun',
            0x06E: 'Martial Arts',
            0x06F: 'Two-Handed Weapon Skill',
            0x070: 'Sword and Shield Skill',
            0x071: 'Single Weapon Skill',
            0x072: 'Two Weapon skill',
            0x073: 'Club',
            0x074: 'Extra Proficiency 2',
            0x075: 'Extra Proficiency 3',
            0x076: 'Extra Proficiency 4',
            0x077: 'Extra Proficiency 5',
            0x078: 'Extra Proficiency 6',
            0x079: 'Extra Proficiency 7',
            0x07A: 'Extra Proficiency 8',
            0x07B: 'Extra Proficiency 9',
            0x07C: 'Extra Proficiency 10',
            0x07D: 'Extra Proficiency 11',
            0x07E: 'Extra Proficiency 12',
            0x07F: 'Extra Proficiency 13',
            0x080: 'Extra Proficiency 14',
            0x081: 'Extra Proficiency 15',
            0x082: 'Extra Proficiency 16',
            0x083: 'Extra Proficiency 17',
            0x084: 'Extra Proficiency 18',
            0x085: 'Extra Proficiency 19',
            0x086: 'Extra Proficiency 20'
            }

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
              'mask': { 0x0001: 'Critical/Unsellable', 0x0002: 'TwoHanded', 0x0004: 'Movable', 0x0008: 'Displayable', 0x0010: 'Cursed', 0x0020: 'Copyable', 0x0040: 'Magical', 0x0080: 'Bow', 0x0100: 'Silver', 0x0200: 'ColdIron', 0x0400: 'Stolen/Unsellable', 0x0800: 'Conversable' },
              'label': 'Flags'},

            { 'key': 'item_type',
              'type': 'WORD',
              'off': 0x001C,
              'enum': item_types,
              'label': 'Item type'},

            { 'key': 'usability_mask',
              'type': 'DWORD',
              'off': 0x001E,
              'mask': { 
                       0x00000001: 'Chaotic...',
                       0x00000002: '...Evil',
                       0x00000004: '...Good',
                       0x00000008: '...Neutral',
                       0x00000010: 'Lawful...',
                       0x00000020: 'Neutral...',
                       0x00000040: 'Bard',
                       0x00000080: 'Cleric',
                       0x00000100: 'Cleric/Mage',
                       0x00000200: 'Cleric/Thief',
                       0x00000400: 'Cleric/Ranger',
                       0x00000800: 'Fighter',
                       0x00001000: 'Fighter/Druid',
                       0x00002000: 'Fighter/Mage',
                       0x00004000: 'Fighter/Cleric',
                       0x00008000: 'Fighter/Mage/Cleric',
                       0x00010000: 'Figter/Mage/Thief',
                       0x00020000: 'Fighter/Thief',
                       0x00040000: 'Mage',
                       0x00080000: 'Mage/Thief',
                       0x00100000: 'Paladin',
                       0x00200000: 'Ranger',
                       0x00400000: 'Thief',
                       0x00800000: 'Elf',
                       0x01000000: 'Dwarf',
                       0x02000000: 'Half-Elf',
                       0x04000000: 'Halfling',
                       0x08000000: 'Human',
                       0x10000000: 'Gnome',
                       0x20000000: 'Monk',
                       0x40000000: 'Druid',
                       0x80000000: 'Half-Orc',
                       },
              'label': 'Unusable by'},

            { 'key': 'item_animation',
              'type': 'STR2',
              'off': 0x0022,
              'enum': {
                    '  ': 'Nothing', 
                    '2A': 'Leather armor', 
                    '3A': 'Chainmail', 
                    '4A': 'Plate mail',
                    '2W': 'Robe',
                    '3W': 'Robe',
                    '4W': 'Robe',
                    'AX': 'Axe',
                    'BW': 'Bow',
                    'CB': 'Crossbow',
                    'CL': 'Club', 
                    'D1': 'Buckler',
                    'D2': 'Shield (small)',
                    'D3': 'Shie;d (medium)',
                    'D4': 'Shield (large)',
                    'DD': 'Dagger', 
                    'FL': 'Flail',
                    'FS': 'Flame sword',
                    'H0': 'Small vertical horns',
                    'H1': 'Large horizontal horns',
                    'H2': 'Feather wings',
                    'H3': 'Top plume',
                    'H4': 'Dragon wings',
                    'H5': 'Feather sideburns',
                    'H6': 'Large curved horns',
                    'HB': 'Halberd',
                    'MC': 'Mace',
                    'MS': 'Morningstar',
                    'QS': 'Quarterstaff (metal)',
                    'S1': 'Sword 1-handed',
                    'S2': 'Sword 2-handed',
                    'S3': 'Katana',
                    'SC': 'Scimitar',
                    'SL': 'Sling',
                    'SP': 'Spear',
                    'SS': 'Short sword',
                    'WH': 'War hammer', 
                    },
              'label': 'Item animation'},

            { 'key': 'min_level',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Min level'},

            { 'key': 'unknown_25', # FIXME: IESDP: is not if just high byte of  0x26 like in V1.1?
              'type': 'BYTE',
              'off': 0x0025,
              'label': 'Unknown 25'},

            { 'key': 'min_str',
              'type': 'BYTE',
              'off': 0x0026,
              'label': 'Min strength (unused in BG1)'},

            { 'key': 'unknown_27', # FIXME: IESDP: is not if just high byte of  0x26 like in V1.1?
              'type': 'BYTE',
              'off': 0x0027,
              'label': 'Unknown 27'},

            { 'key': 'min_str_bonus',
              'type': 'BYTE',
              'off': 0x0028,
              'label': 'Min strength bonus (unused in BG1)'},

            { 'key': 'kit_usability_1',
              'type': 'BYTE',
              'off': 0x0029,
              'mask': kit_usability_mask_1,
              'label': 'Kit usability 1'},

            { 'key': 'min_int',
              'type': 'BYTE',
              'off': 0x002A,
              'label': 'Min intelligence (unused in BG1)'},

            { 'key': 'kit_usability_2',
              'type': 'BYTE',
              'off': 0x002B,
              'mask': kit_usability_mask_2,
              'label': 'Kit usability 2'},

            { 'key': 'min_dex',
              'type': 'BYTE',
              'off': 0x002C,
              'label': 'Min dexterity (unused in BG1)'},

            { 'key': 'kit_usability_3',
              'type': 'BYTE',
              'off': 0x002D,
              'mask': kit_usability_mask_3,
              'label': 'Kit usability 3'},

            { 'key': 'min_wis',
              'type': 'BYTE',
              'off': 0x002E,
              'label': 'Min wisdom (unused in BG1)'},

            { 'key': 'kit_usability_4',
              'type': 'BYTE',
              'off': 0x002F,
              'mask': kit_usability_mask_4,
              'label': 'Kit usability 4'},

            { 'key': 'min_con',
              'type': 'BYTE',
              'off': 0x0030,
              'label': 'Min constitution (unused in BG1)'},

            { 'key': 'weapon_proficiency',
              'type': 'BYTE',
              'off': 0x0031,
              'enum': weapon_proficiencies,
              'label': 'Weapon proficiency'},

            { 'key': 'min_cha',
              'type': 'BYTE',
              'off': 0x0032,
              'label': 'Min charisma'}, # FIXME: IESDP: is it actually USED in BG1?

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
              'enum': { 0: 'None', 1: 'Arrow', 2: 'Bolt', 3: 'Bullet', 40: 'Spear', 100: 'Throwing axe' },
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
              'enum': { 0: 'None', 1: 'Piercing/Magic', 2: 'Blunt', 3: 'Slashing', 4: 'Ranged', 5: 'Fists', 6: 'Piercing/Blunt', 7: 'Piercing/Slashing', 8: 'Blunt/Slashing' },
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
              'mask': {
                      0x0001: 'Add strength bonus',
                      0x0002: 'Breakable',
                      0x0004: 'EE: Damage strength bonus',
                      0x0008: 'EE: THAC0 strength bonus',
                      0x0400: 'Hostile',
                      0x0800: 'Recharges'
                      },
              'label': 'Flags'},

            { 'key': 'unknown_28',
              'type': 'WORD',
              'off': 0x0028,
              'label': 'Unknown 28'},

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
              'enum': 'effects', # FIXME: this ids file does not exist
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
              'type': 'DWORD',
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
        size_extended = self.get_struc_size (self.extended_header_desc)
        size_feature = self.get_struc_size (self.feature_desc)
        
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

        
register_format (ITM_V10_Format, signature='ITM V1  ')
