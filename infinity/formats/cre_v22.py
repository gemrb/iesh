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


from infinity.format import Format, register_format


class CRE_V22_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'long_name',
              'type': 'STRREF',
              'off': 0x0008,
              'label': 'Long creature name'},

            { 'key': 'short_name',
              'type': 'STRREF',
              'off': 0x000C,
              'label': 'Short creature name'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0010,
              'mask': {
                       0x0001: 'Dmg doesn\'t stop casting',
                       0x0002: 'No corpse',
                       0x0004: 'Keep corpse',
                       0x0008: 'Orig class Fighter',
                       0x0010: 'Orig class Mage',
                       0x0020: 'Orig class Cleric',
                       0x0040: 'Orig class Thief',
                       0x0080: 'Orig class Druid',
                       0x0100: 'Orig class Ranger',
                       0x0200: 'Fallen Paladin',
                       0x0400: 'Fallen Ranger',
                       0x0800: 'Exportable',
                       0x1000: 'Unknown bit12',
                       0x2000: 'Quest-critical',
                       0x4000: 'Can activate non-NPC triggers',
                       0x8000: 'Enabled',
                       0x00010000: 'Seen party',
                       0x00020000: 'Invulnerable',
                       0x00040000: 'Non-threatening enemy',
                       0x00080000: 'No talk',
                       0x00100000: 'Ignore Return to start',
                       0x00200000: 'Ignore Inhibit AI',
                       0x00400000: 'unused bit22',
                       0x00800000: 'unused bit23',
                       0x40000000: 'corpse related?',
                       },
              'label': 'Creature flags'},

            { 'key': 'xp',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'XP'},

            { 'key': 'power_level',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Creature power level / XP'},

            { 'key': 'gold',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Gold carried'},

            { 'key': 'permanent_status_flags',
              'type': 'DWORD',
              'off': 0x0020,
              'enum': 'STATE',
              'label': 'Permanent status flags'},  # as per STATE.IDS

            { 'key': 'current_hp',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Current HP'},

            { 'key': 'max_hp',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Maximum HP'},

            { 'key': 'animation_id',
              'type': 'DWORD',
              'off': 0x0028,
              'enum': 'ANIMATE',
              'label': 'Animation ID'},  # as per ANIMATE.IDS

            { 'key': 'metal_color_index',
                'type': 'BYTE',
                'off': 0x002C,
                'label': 'Metal color index (BG1 anim)' },

            { 'key': 'minor_color_index',
                'type': 'BYTE',
                'off': 0x002D,
                'label': 'Minor color index (BG1 anim)' },

            { 'key': 'major_color_index',
                'type': 'BYTE',
                'off': 0x002E,
                'label': 'Major color index (BG1 anim)' },

            { 'key': 'skin_color_index',
                'type': 'BYTE',
                'off': 0x002F,
                'label': 'Skin color index (BG1 anim)' },

            { 'key': 'leather_color_index',
                'type': 'BYTE',
                'off': 0x0030,
                'label': 'Leather color index (BG1 anim)' },

            { 'key': 'armor_color_index',
                'type': 'BYTE',
                'off': 0x0031,
                'label': 'Armor color index (BG1 anim)' },

            { 'key': 'hair_color_index',
                'type': 'BYTE',
                'off': 0x0032,
                'label': 'Hair color index (BG1 anim)' },

            { 'key': 'eff_structure_version',
                'type': 'BYTE',
                'off': 0x0033,
                'enum': { 0: 'Version 1', 1: 'Version 2' },
                'label': 'EFF structure version' },

            { 'key': 'small_portrait_resref',
                'type': 'RESREF',
                'off': 0x0034,
                'label': 'Small portrait resref' },

            { 'key': 'large_portrait_resref',
                'type': 'RESREF',
                'off': 0x003C,
                'label': 'Large portrait resref' },

            { 'key': 'reputation',
                'type': 'BYTE',  # FIXME: actually it's a signed byte
                'off': 0x0044,
                'label': 'Reputation' },

            { 'key': 'hide_in_shadows',
                'type': 'BYTE',
                'off': 0x0045,
                'label': 'Hide in shadows (base)' },

            { 'key': 'armor_class',  # or Natural AC?
                'type': 'WORD',
                'off': 0x0046,
                'label': 'Armor class' },

            { 'key': 'armor_class_crushing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x0048,
                'label': 'Armor class (crushing att mod)' },

            { 'key': 'armor_class_missile_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004A,
                'label': 'Armor class (missile att mod)' },

            { 'key': 'armor_class_piercing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004C,
                'label': 'Armor class (piercing att mod)' },

            { 'key': 'armor_class_slashing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004E,
                'label': 'Armor class (slashing att mod)' },

            { 'key': 'bab',
                'type': 'BYTE',
                'off': 0x0050,
                'label': 'Base attack bonus (BAB) for NPC' },

            { 'key': 'num_attacks',
                'type': 'BYTE',
                'off': 0x0051,
                'label': 'Number of attacks (0-10)' },

            { 'key': 'save_vs_fortitude',
                'type': 'BYTE',
                'off': 0x0052,
                'label': 'Save versus fortitude (0-20)' },

            { 'key': 'save_vs_reflex',
                'type': 'BYTE',
                'off': 0x0053,
                'label': 'Save versus reflex (0-20)' },

            { 'key': 'save_vs_will',
                'type': 'BYTE',
                'off': 0x0054,
                'label': 'Save versus will (0-20)' },

            { 'key': 'resist_fire',
                'type': 'BYTE',
                'off': 0x0055,
                'label': 'Resist fire (0-100)' },

            { 'key': 'resist_cold',
                'type': 'BYTE',
                'off': 0x0056,
                'label': 'Resist cold (0-100)' },

            { 'key': 'resist_electricity',
                'type': 'BYTE',
                'off': 0x0057,
                'label': 'Resist electricity (0-100)' },

            { 'key': 'resist_acid',
                'type': 'BYTE',
                'off': 0x0058,
                'label': 'Resist acid (0-100)' },

            { 'key': 'resist_magic',
                'type': 'BYTE',
                'off': 0x0059,
                'label': 'Resist magic (0-100)' },

            { 'key': 'resist_magic_fire',
                'type': 'BYTE',
                'off': 0x005A,
                'label': 'Resist magic fire (0-100)' },

            { 'key': 'resist_magic_cold',
                'type': 'BYTE',
                'off': 0x005B,
                'label': 'Resist magic cold (0-100)' },

            { 'key': 'resist_slashing',
                'type': 'BYTE',
                'off': 0x005C,
                'label': 'Resist slashing (0-100)' },

            { 'key': 'resist_crushing',
                'type': 'BYTE',
                'off': 0x005D,
                'label': 'Resist crushing (0-100)' },

            { 'key': 'resist_piercing',
                'type': 'BYTE',
                'off': 0x005E,
                'label': 'Resist piercing (0-100)' },

            { 'key': 'resist_missile',
                'type': 'BYTE',
                'off': 0x005F,
                'label': 'Resist missile (0-100)' },

            { 'key': 'resist_magic_damage',
                'type': 'BYTE',
                'off': 0x0060,
                'label': 'Resist magic damage (0-100)' },

            { 'key': 'unknown_61',
                'type': 'BYTE',
                'off': 0x0061,
                'count': 4,
                'label': 'Unknown 61. Further resistances?' },

            { 'key': 'fatigue',
                'type': 'BYTE',
                'off': 0x0065,
                'label': 'Fatigue' },

            { 'key': 'intoxication',
                'type': 'BYTE',
                'off': 0x0066,
                'label': 'Intoxication' },

            { 'key': 'luck',
                'type': 'BYTE',
                'off': 0x0067,
                'label': 'Luck' },

            { 'key': 'turn_undead_level',
                'type': 'BYTE',
                'off': 0x0068,
                'label': 'Turn undead level' },

            { 'key': 'unknown_69',
                'type': 'BYTE',
                'off': 0x0069,
                'count': 33,
                'label': 'Unknown69' },

            { 'key': 'level',
                'type': 'BYTE',
                'off': 0x008a,
                'label': 'Total levels' },


            { 'key': 'barbarian_levels',
                'type': 'BYTE',
                'off': 0x008b,
                'label': 'Barbarian levels' },

            { 'key': 'bard_levels',
                'type': 'BYTE',
                'off': 0x008c,
                'label': 'Bard levels' },

            { 'key': 'cleric_levels',
                'type': 'BYTE',
                'off': 0x008d,
                'label': 'Cleric levels' },

            { 'key': 'druid_levels',
                'type': 'BYTE',
                'off': 0x008e,
                'label': 'Druid levels' },

            { 'key': 'fighter_levels',
                'type': 'BYTE',
                'off': 0x008f,
                'label': 'Fighter levels' },

            { 'key': 'monk_levels',
                'type': 'BYTE',
                'off': 0x0090,
                'label': 'Monk levels' },

            { 'key': 'paladin_levels',
                'type': 'BYTE',
                'off': 0x0091,
                'label': 'Paladin levels' },

            { 'key': 'ranger_levels',
                'type': 'BYTE',
                'off': 0x0092,
                'label': 'Ranger levels' },

            { 'key': 'rogue_levels',
                'type': 'BYTE',
                'off': 0x0093,
                'label': 'Rogue levels' },

            { 'key': 'sorcerer_levels',
                'type': 'BYTE',
                'off': 0x0094,
                'label': 'Sorcerer levels' },

            { 'key': 'wizard_levels',
                'type': 'BYTE',
                'off': 0x0095,
                'label': 'wizard levels' },

            { 'key': 'unknown_96',
                'type': 'BYTE',
                'off': 0x0096,
                'count': 22,
                'label': 'Unknown 96' },

            { 'key': 'strref',
                'type': 'STRREF',
                'off': 0x00AC,
                'count': 64,
                'label': 'Strref' },

            { 'key': 'team_script',
                'type': 'RESREF',
                'off': 0x01AC,
                'label': 'Team script' },

            { 'key': 'special_script_1',
                'type': 'RESREF',
                'off': 0x01B4,
                'label': 'Special script 1' },

            { 'key': 'creature_enchantment_level',
                'type': 'BYTE',
                'off': 0x01BC,
                'label': 'Creature enchantment level' },

            { 'key': 'unknown_1bd',
                'type': 'BYTE',
                'off': 0x01BD,
                'count': 3,
                'label': 'Unknown 1BD' },

            { 'key': 'feats_1',
                'type': 'DWORD',
                'off': 0x01C0,
                'label': 'Feats 1' },

            { 'key': 'feats_2',
                'type': 'DWORD',
                'off': 0x01C4,
                'label': 'Feats 2' },

            { 'key': 'feats_3',
                'type': 'DWORD',
                'off': 0x01C8,
                'label': 'Feats 3' },

            { 'key': 'unknown_1cc',
                'type': 'DWORD',
                'off': 0x01CC,
                'count': 3,
                'label': 'Unknown 1CC' },

            { 'key': 'mw_bow',
                'type': 'BYTE',
                'off': 0x01D8,
                'label': 'MW: Bow' },

            { 'key': 'sw_crossbow',
                'type': 'BYTE',
                'off': 0x01D9,
                'label': 'SW: Crossbow' },

            { 'key': 'sw_missile',
                'type': 'BYTE',
                'off': 0x01DA,
                'label': 'SW: Missile' },

            { 'key': 'mw_axe',
                'type': 'BYTE',
                'off': 0x01DB,
                'label': 'MW: Axe' },

            { 'key': 'sw_mace',
                'type': 'BYTE',
                'off': 0x01DC,
                'label': 'SW: Mace' },

            { 'key': 'mw_flail',
                'type': 'BYTE',
                'off': 0x01DD,
                'label': 'MW: Flail' },

            { 'key': 'mw_polearm',
                'type': 'BYTE',
                'off': 0x01DE,
                'label': 'MW: Polearm' },

            { 'key': 'mw_hammer',
                'type': 'BYTE',
                'off': 0x01DF,
                'label': 'MW: Hammer' },

            { 'key': 'sw_quarterstaff',
                'type': 'BYTE',
                'off': 0x01E0,
                'label': 'SW: Quarterstaff' },

            { 'key': 'mw_greatsword',
                'type': 'BYTE',
                'off': 0x01E1,
                'label': 'MW: Greatsword' },

            { 'key': 'mw_large_sword',
                'type': 'BYTE',
                'off': 0x01E2,
                'label': 'MW: Large sword' },

            { 'key': 'sw_small_blade',
                'type': 'BYTE',
                'off': 0x01E3,
                'label': 'SW: Small blade' },

            { 'key': 'toughness',
                'type': 'BYTE',
                'off': 0x01E4,
                'label': 'Toughness' },

            { 'key': 'armored_arcana',
                'type': 'BYTE',
                'off': 0x01E5,
                'label': 'Armored Arcana' },

            { 'key': 'cleave',
                'type': 'BYTE',
                'off': 0x01E6,
                'label': 'Cleave' },

            { 'key': 'armor_proficiency',
                'type': 'BYTE',
                'off': 0x01E7,
                'label': 'Armor Proficiency' },

            { 'key': 'sf_enchantment',
                'type': 'BYTE',
                'off': 0x01E8,
                'label': 'SF: Enchantment' },

            { 'key': 'sf_evocation',
                'type': 'BYTE',
                'off': 0x01E9,
                'label': 'SF: Evocation' },

            { 'key': 'sf_necromancy',
                'type': 'BYTE',
                'off': 0x01EA,
                'label': 'SF: Necromancy' },

            { 'key': 'sf_transmutation',
                'type': 'BYTE',
                'off': 0x01EB,
                'label': 'SF: Transmutation' },

            { 'key': 'spell_penetration',
                'type': 'BYTE',
                'off': 0x01EC,
                'label': 'Spell Penetration' },

            { 'key': 'extra_rage',
                'type': 'BYTE',
                'off': 0x01ED,
                'label': 'Extra Rage' },

            { 'key': 'extra_wild_shape',
                'type': 'BYTE',
                'off': 0x01EE,
                'label': 'Extra Wild Shape' },

            { 'key': 'extra_smiting',
                'type': 'BYTE',
                'off': 0x01EF,
                'label': 'Extra Smiting' },

            { 'key': 'extra_turning',
                'type': 'BYTE',
                'off': 0x01F0,
                'label': 'Extra Turning' },

            { 'key': 'ew_bastard_sword',
                'type': 'BYTE',
                'off': 0x01F1,
                'label': 'EW: Bastard Sword' },

            { 'key': 'unknown_1f2',
                'type': 'BYTES',
                'off': 0x01F2,
                'size': 38,
                'label': 'Unknown 1F2' },

            { 'key': 'alchemy',
                'type': 'BYTE',
                'off': 0x0218,
                'label': 'Alchemy' },

            { 'key': 'animal_empathy',
                'type': 'BYTE',
                'off': 0x0219,
                'label': 'Animal Empathy' },

            { 'key': 'bluff',
                'type': 'BYTE',
                'off': 0x021A,
                'label': 'Bluff' },

            { 'key': 'concentration',
                'type': 'BYTE',
                'off': 0x021B,
                'label': 'Concentration' },

            { 'key': 'diplomacy',
                'type': 'BYTE',
                'off': 0x021C,
                'label': 'Diplomacy' },

            { 'key': 'disable_device',
                'type': 'BYTE',
                'off': 0x021D,
                'label': 'Disable Device' },

            { 'key': 'hide',
                'type': 'BYTE',
                'off': 0x021E,
                'label': 'Hide' },

            { 'key': 'intimidate',
                'type': 'BYTE',
                'off': 0x021F,
                'label': 'Intimidate' },

            { 'key': 'knowledge_arcana',
                'type': 'BYTE',
                'off': 0x0220,
                'label': 'Knowledge (arcana)' },

            { 'key': 'move_silently',
                'type': 'BYTE',
                'off': 0x0221,
                'label': 'Move Silently' },

            { 'key': 'open_lock',
                'type': 'BYTE',
                'off': 0x0222,
                'label': 'Open Lock' },

            { 'key': 'pick_pocket',
                'type': 'BYTE',
                'off': 0x0223,
                'label': 'Pick Pocket' },

            { 'key': 'search',
                'type': 'BYTE',
                'off': 0x0224,
                'label': 'Search' },

            { 'key': 'spellcraft',
                'type': 'BYTE',
                'off': 0x0225,
                'label': 'Spellcraft' },

            { 'key': 'use_magic_device',
                'type': 'BYTE',
                'off': 0x0226,
                'label': 'Use Magic Device' },

            { 'key': 'wilderness_law',
                'type': 'BYTE',
                'off': 0x0227,
                'label': 'Wilderness Law' },

            { 'key': 'unknown_228',
                'type': 'BYTES',
                'off': 0x0228,
                'size': 50,
                'label': 'Unknown 228' },

            { 'key': 'xp_category',
                'type': 'BYTE',
                'off': 0x025A,
                'label': 'XP category (MONCRATE.2DA)' },

            { 'key': 'favoured_enemy_1',
                'type': 'BYTE',
                'off': 0x025B,
                'label': 'Favoured Enemy 1' },

            { 'key': 'favoured_enemy_2',
                'type': 'BYTE',
                'off': 0x025C,
                'label': 'Favoured Enemy 2' },

            { 'key': 'favoured_enemy_3',
                'type': 'BYTE',
                'off': 0x025D,
                'label': 'Favoured Enemy 3' },

            { 'key': 'favoured_enemy_4',
                'type': 'BYTE',
                'off': 0x025E,
                'label': 'Favoured Enemy 4' },

            { 'key': 'favoured_enemy_5',
                'type': 'BYTE',
                'off': 0x025F,
                'label': 'Favoured Enemy 5' },

            { 'key': 'favoured_enemy_6',
                'type': 'BYTE',
                'off': 0x0260,
                'label': 'Favoured Enemy 6' },

            { 'key': 'favoured_enemy_7',
                'type': 'BYTE',
                'off': 0x0261,
                'label': 'Favoured Enemy 7' },

            { 'key': 'favoured_enemy_8',
                'type': 'BYTE',
                'off': 0x0262,
                'label': 'Favoured Enemy 8' },

            { 'key': 'subrace',
                'type': 'BYTE',
                'off': 0x0263,
                'enum': 'SUBRACE',
                'label': 'Subrace (SUBRACE.IDS)' },

            { 'key': 'unknown_264',
                'type': 'BYTES',
                'off': 0x0264,
                'size': 2,
                'label': 'Unknown 264' },

            { 'key': 'strength',
                'type': 'BYTE',
                'off': 0x0266,
                'label': 'Strength' },

            { 'key': 'intelligence',
                'type': 'BYTE',
                'off': 0x0267,
                'label': 'Intelligence' },

            { 'key': 'wisdom',
                'type': 'BYTE',
                'off': 0x0268,
                'label': 'Wisdom' },

            { 'key': 'dexterity',
                'type': 'BYTE',
                'off': 0x0269,
                'label': 'Dexterity' },

            { 'key': 'constitution',
                'type': 'BYTE',
                'off': 0x026A,
                'label': 'Constitution' },

            { 'key': 'charisma',
                'type': 'BYTE',
                'off': 0x026B,
                'label': 'Charisma' },

            { 'key': 'unknown_26c',
                'type': 'BYTES',
                'off': 0x026C,
                'size': 4,
                'label': 'Unknown 26C' },

            { 'key': 'kit',
                'type': 'DWORD',
                'off': 0x0270,
                'label': 'Kit (bitfield)' },

            { 'key': 'cre_script_override',
                'type': 'RESREF',
                'off': 0x0274,
                'label': 'Creature script - Override' },

            { 'key': 'cre_script_special_3',
                'type': 'RESREF',
                'off': 0x027C,
                'label': 'Creature script - Special Script 3' },

            { 'key': 'cre_script_special_2',
                'type': 'RESREF',
                'off': 0x0284,
                'label': 'Creature script - Special Script 2' },

            { 'key': 'cre_script_combat',
                'type': 'RESREF',
                'off': 0x028C, # FIXME: iesdp error!
                'label': 'Creature script - Combat Script' },

            { 'key': 'cre_script_movement',
                'type': 'RESREF',
                'off': 0x0294,
                'label': 'Creature script - Movement Script' },

            { 'key': 'visible',
                'type': 'BYTE',
                'off': 0x029C,
                'label': 'Visible' },

            { 'key': 'set_death_var_on_death',
                'type': 'BYTE',
                'off': 0x029D,
                'label': 'Set <scriptname>_DEAD on death' },

            { 'key': 'set_kill_cnt_on_death',
                'type': 'BYTE',
                'off': 0x029E,
                'label': 'Set KILL_<racename>_CNT on death' },

            { 'key': 'unknown_29f',
                'type': 'BYTE',
                'off': 0x029F,
                'label': 'Unknown 29F' },

            { 'key': 'internals',
                'type': 'WORD',
                'off': 0x02A0,
                'count': 5,
                'label': 'Internals' },

            { 'key': 'secondary_death_var',
                'type': 'STR32',
                'off': 0x02AA,
                'label': 'Secondary death variable' },

            { 'key': 'tertiary_death_var',
                'type': 'STR32',
                'off': 0x02CA,
                'label': 'Tertiary death variable' },

            { 'key': 'unknown_2ea',
                'type': 'WORD',
                'off': 0x02EA,
                'label': 'Unknown 2EA' },

            { 'key': 'saved_location_x_coordinate',
                'type': 'WORD',
                'off': 0x02EC,
                'label': 'Saved Location X coordinate' },

            { 'key': 'saved_location_y_coordinate',
                'type': 'WORD',
                'off': 0x02EE, # FIXME: iesdp error
                'label': 'Saved Location Y coordinate' },

            { 'key': 'saved_location_orientation',
                'type': 'WORD',
                'off': 0x02F0,
                'label': 'Saved Location orientation' },

            { 'key': 'unknown_2f2',
                'type': 'BYTES',
                'off': 0x02F2,
                'size': 15,
                'label': 'Unknown 2F2' },

            { 'key': 'minimum_transparency',
                'type': 'BYTE',
                'off': 0x0301,
                'label': 'Minimum transparency' },

            { 'key': 'fade_speed',
                'type': 'BYTE',
                'off': 0x0302,
                'label': 'Fade speed' },

            { 'key': 'specflag_values',
                'type': 'BYTE',
                'off': 0x0303,
                'mask': { 0x01: 'Auto concentration succ, no morale fail', 
                          0x02: 'Immune to crit hits', 
                          0x04: 'Disallow paladin in LU', 
                          0x08: 'Disallow monk in LU' },
                'label': 'Specflag values' },

            { 'key': 'visible',
                'type': 'BYTE',
                'off': 0x0304,
                'label': 'Visible' },

            { 'key': 'unknown_305',
                'type': 'BYTE',
                'off': 0x0305,
                'label': 'Unknown 305' },

            { 'key': 'unknown_306',
                'type': 'BYTE',
                'off': 0x0306,
                'label': 'Unknown 306' },

            { 'key': 'remaining_skill_points',
                'type': 'BYTE',
                'off': 0x0307,
                'label': 'Remaining skill points' },

            { 'key': 'unknown_308',
                'type': 'BYTES',
                'off': 0x0308,
                'size': 124,
                'label': 'Unknown 308' },

            { 'key': 'ea',
                'type': 'BYTE',
                'off': 0x0384,
                'enum': 'EA',
                'label': 'Enemy-Ally (EA.IDS)' },

            { 'key': 'general',
                'type': 'BYTE',
                'off': 0x0385,
                'enum': 'GENERAL',
                'label': 'General (GENERAL.IDS)' },

            { 'key': 'race',
                'type': 'BYTE',
                'off': 0x0386,
                'enum': 'RACE',
                'label': 'Race (RACE.IDS)' },

            { 'key': 'class',
                'type': 'BYTE',
                'off': 0x0387,
                'enum': 'CLASS',
                'label': 'Class (CLASS.IDS)' },

            { 'key': 'specific',
                'type': 'BYTE',
                'off': 0x0388,
                'enum': 'SPECIFIC',
                'label': 'Specific (SPECIFIC.IDS)' },

            { 'key': 'sex',
                'type': 'BYTE',
                'off': 0x0389,
                'enum': 'GENDER',
                'label': 'Sex (GENDER.IDS)' },

            { 'key': 'object_ids_references',
                'type': 'BYTE',
                'off': 0x038A,
                'count': 5,
                'enum': 'OBJECT',
                'label': 'OBJECT.IDS references' },

            { 'key': 'alignment',
                'type': 'BYTE',
                'off': 0x038F,
                'enum': 'ALIGNMEN',
                'label': 'Alignment (ALIGNMEN.IDS)' },

            { 'key': 'global_actor_enumeration_value',
                'type': 'WORD',
                'off': 0x0390,
                'label': 'Global actor enumeration value' },

            { 'key': 'local_actor_enumeration_value',
                'type': 'WORD',
                'off': 0x0392,
                'label': 'Local (area) actor enumeration value' },

            { 'key': 'death_var',
                'type': 'STR32',
                'off': 0x0394,
                'label': 'Death Variable' },

            { 'key': 'avclass_value',
                'type': 'WORD',
                'off': 0x03B4,
                'label': 'AVClass value' },

            { 'key': 'classmsk_bitfield_value',
                'type': 'WORD',
                'off': 0x03B6,
                'label': 'ClassMsk bitfield value' },

            { 'key': 'unknown_3b8',
                'type': 'WORD',
                'off': 0x03B8,
                'label': 'Unknown 3B8' },

            { 'key': 'bard_spell_offset',
                'type': 'DWORD',
                'off': 0x03BA,
                'count': 9,
                'label': 'Bard Spell Offset' },

            { 'key': 'cleric_spell_offset',
                'type': 'DWORD',
                'off': 0x03DE,
                'count': 9,
                'label': 'Cleric Spell Offset' },

            { 'key': 'druid_spell_offset',
                'type': 'DWORD',
                'off': 0x0402,
                'count': 9,
                'label': 'Druid Spell Offset' },

            { 'key': 'paladin_spell_offset',
                'type': 'DWORD',
                'off': 0x0426,
                'count': 9,
                'label': 'Paladin Spell Offset' },

            { 'key': 'ranger_spell_offset',
                'type': 'DWORD',
                'off': 0x044A,
                'count': 9,
                'label': 'Ranger Spell Offset' },

            { 'key': 'sorcerer_spell_offset',
                'type': 'DWORD',
                'off': 0x046E,
                'count': 9,
                'label': 'Sorcerer Spell Offset' },

            { 'key': 'wizard_spell_offset',
                'type': 'DWORD',
                'off': 0x0492,
                'count': 9,
                'label': 'Wizard Spell Offset' },

            { 'key': 'bard_spell_count',
                'type': 'DWORD',
                'off': 0x04B6,
                'count': 9,
                'label': 'Bard Spell Count' },

            { 'key': 'cleric_spell_count',
                'type': 'DWORD',
                'off': 0x04DA,
                'count': 9,
                'label': 'Cleric Spell Count' },

            { 'key': 'druid_spell_count',
                'type': 'DWORD',
                'off': 0x04FE,
                'count': 9,
                'label': 'Druid Spell Count' },

            { 'key': 'paladin_spell_count',
                'type': 'DWORD',
                'off': 0x0522,
                'count': 9,
                'label': 'Paladin Spell Count' },

            { 'key': 'ranger_spell_count',
                'type': 'DWORD',
                'off': 0x0546,
                'count': 9,
                'label': 'Ranger Spell Count' },

            { 'key': 'sorcerer_spell_count',
                'type': 'DWORD',
                'off': 0x056A,
                'count': 9,
                'label': 'Sorcerer Spell Count' },

            { 'key': 'wizard_spell_count',
                'type': 'DWORD',
                'off': 0x058E,
                'count': 9,
                'label': 'Wizard Spell Count' },

            { 'key': 'domain1_spell_offset',
                'type': 'DWORD',
                'off': 0x05B2,
                'label': 'Domain1 Spell Offset' },

            { 'key': 'domain2_spell_offset',
                'type': 'DWORD',
                'off': 0x05B6,
                'label': 'Domain2 Spell Offset' },

            { 'key': 'domain3_spell_offset',
                'type': 'DWORD',
                'off': 0x05BA,
                'label': 'Domain3 Spell Offset' },

            { 'key': 'domain4_spell_offset',
                'type': 'DWORD',
                'off': 0x05BE,
                'label': 'Domain4 Spell Offset' },

            { 'key': 'domain5_spell_offset',
                'type': 'DWORD',
                'off': 0x05C2,
                'label': 'Domain5 Spell Offset' },

            { 'key': 'domain6_spell_offset',
                'type': 'DWORD',
                'off': 0x05C6,
                'label': 'Domain6 Spell Offset' },

            { 'key': 'domain7_spell_offset',
                'type': 'DWORD',
                'off': 0x05CA,
                'label': 'Domain7 Spell Offset' },

            { 'key': 'domain8_spell_offset',
                'type': 'DWORD',
                'off': 0x05CE,
                'label': 'Domain8 Spell Offset' },

            { 'key': 'domain9_spell_offset',
                'type': 'DWORD',
                'off': 0x05D2,
                'label': 'Domain9 Spell Offset' },

            { 'key': 'domain1_spell_count',
                'type': 'DWORD',
                'off': 0x05D6,
                'label': 'Domain1 Spell Count' },

            { 'key': 'domain2_spell_count',
                'type': 'DWORD',
                'off': 0x05DA,
                'label': 'Domain2 Spell Count' },

            { 'key': 'domain3_spell_count',
                'type': 'DWORD',
                'off': 0x05DE,
                'label': 'Domain3 Spell Count' },

            { 'key': 'domain4_spell_count',
                'type': 'DWORD',
                'off': 0x05E2,
                'label': 'Domain4 Spell Count' },

            { 'key': 'domain5_spell_count',
                'type': 'DWORD',
                'off': 0x05E6,
                'label': 'Domain5 Spell Count' },

            { 'key': 'domain6_spell_count',
                'type': 'DWORD',
                'off': 0x05EA,
                'label': 'Domain6 Spell Count' },

            { 'key': 'domain7_spell_count',
                'type': 'DWORD',
                'off': 0x05EE,
                'label': 'Domain7 Spell Count' },

            { 'key': 'domain8_spell_count',
                'type': 'DWORD',
                'off': 0x05F2,
                'label': 'Domain8 Spell Count' },

            { 'key': 'domain9_spell_count',
                'type': 'DWORD',
                'off': 0x05F6,
                'label': 'Domain9 Spell Count' },

            { 'key': 'ability_off',
                'type': 'DWORD',
                'off': 0x05FA,
                'label': 'Abilities Offset' },

            { 'key': 'ability_cnt',
                'type': 'DWORD',
                'off': 0x05FE,
                'label': 'Abilities Count' },

            { 'key': 'song_off',
                'type': 'DWORD',
                'off': 0x0602,
                'label': 'Song Offset' },

            { 'key': 'song_cnt',
                'type': 'DWORD',
                'off': 0x0606,
                'label': 'Song Count' },

            { 'key': 'shape_off',
                'type': 'DWORD',
                'off': 0x060A,
                'label': 'Shapes Offset' },

            { 'key': 'shape_cnt',
                'type': 'DWORD',
                'off': 0x060E,
                'label': 'Shapes Count' },

            { 'key': 'item_slot_off',
                'type': 'DWORD',
                'off': 0x0612,
                'label': 'Item slots Offset' },

            { 'key': 'item_off',
                'type': 'DWORD',
                'off': 0x0616,
                'label': 'Item Offset' },

            { 'key': 'item_cnt',
                'type': 'DWORD',
                'off': 0x061A,
                'label': 'Item Count' },

            { 'key': 'effect_off',
                'type': 'DWORD',
                'off': 0x061E,
                'label': 'Effects Offset' },

            { 'key': 'effect_cnt',
                'type': 'DWORD',
                'off': 0x0622,
                'label': 'Effects Count' },

            { 'key': 'dialog',
                'type': 'RESREF',
                'off': 0x0626,
                'label': 'Dialog' },
        )

    known_spell_desc = (
            { 'key': 'spell_index',
                'type': 'DWORD',
                'off': 0x0000,
                'label': 'Spell index into relevant LIST*.2DA)' },

            { 'key': 'amount_memorized',
                'type': 'DWORD',
                'off': 0x0004,
                'label': 'Amount memorized' },

            { 'key': 'amount_remaining',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Amount remaining' },

            { 'key': 'unknown_0c',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Unknown 0C' },

            )

    spell_memorization_desc = (
            { 'key': 'total_memorization_slots',
                'type': 'DWORD',
                'off': 0x0000,
                'label': 'Total memorization slots' },

            { 'key': 'free_memorization_slots',
                'type': 'DWORD',
                'off': 0x0004,
                'label': 'Free memorization slots' },

            )


    item_desc = (
            { 'key': 'item_resref',
                'type': 'RESREF',
                'restype': 'ITM',
                'off': 0x0000,
                'label': 'ITM resref' },

            { 'key': 'expiration_time_1',
                'type': 'BYTE',
                'off': 0x0008,
                'label': 'Expiration time - creation hour' },

            { 'key': 'expiration_time_2',
                'type': 'BYTE',
                'off': 0x0009,
                'label': 'Expiration time - (elapsed hours/256) + 1' },

            { 'key': 'usage_1',
                'type': 'WORD',
                'off': 0x000A,
                'label': 'Usage 1' },

            { 'key': 'usage_2',
                'type': 'WORD',
                'off': 0x000C,
                'label': 'Usage 2' },

            { 'key': 'usage_3',
                'type': 'WORD',
                'off': 0x000E,
                'label': 'Usage 3' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0010,
                'mask': { 0x01: 'Identified', 0x02: 'Unstealable', 0x04: 'Stolen', 0x08: 'Magical' },
                'label': 'Flags' },
    )

    item_slot_desc = (
            { 'key': 'item',
                'type': 'WORD',
                'off': 0x0000,
                'count': 50,
                'label': 'Item' },

            { 'key': 'selected_weapon', # IESDP: Values are from slots.ids - 35, with 1000 meaning "fist".
                'type': 'WORD',
                'off': 0x0064,
                'label': 'Selected Weapon' },

            { 'key': 'selected_weapon_ability',
                'type': 'WORD',
                'off': 0x0066,
                'label': 'Selected Weapon Ability' },
    )

    # classes that have spells
    magic_class_keys = ('bard', 'cleric', 'druid','paladin','ranger', 'sorcerer', 'wizard')


    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'CRE'

        self.known_spells = None
        self.domain_spells = None
        self.item_list = []
        self.slots = None


    def read (self, stream):
        self.read_header (stream)

        self.known_spells = {}
        for key in self.magic_class_keys:
            self.known_spells[key] = []
            for i, (cnt, off) in enumerate(zip(self.header[key+'_spell_count'], self.header[key+'_spell_offset'])):
                spells = []
                for j in range(cnt):
                    obj = {}
                    self.read_struc (stream, off, self.known_spell_desc, obj)
                    spells.append(obj)
                    off += self.get_struc_size(self.known_spell_desc)

                obj2 = {}
                self.read_struc (stream, off, self.spell_memorization_desc, obj2)

                self.known_spells[key].append({ 'spells': spells, 'memorization_info': obj2 })

        self.domain_spells = {}
        for key in range(1, 10):
            cnt, off = self.header['domain%d_spell_count' %key], self.header['domain%d_spell_offset' %key]  
            spells = []
            for j in range(cnt):
                obj = {}
                self.read_struc (stream, off, self.known_spell_desc, obj)
                spells.append(obj)
                off += self.get_struc_size(self.known_spell_desc)

            obj2 = {}
            self.read_struc (stream, off, self.spell_memorization_desc, obj2)

            self.domain_spells[key] = { 'spells': spells, 'memorization_info': obj2 }

        self.abilities = {}
        for key in ('ability', 'song', 'shape'):
            cnt, off = self.header['%s_cnt' %key], self.header['%s_off' %key]  
            spells = []
            for j in range(cnt):
                obj = {}
                self.read_struc (stream, off, self.known_spell_desc, obj)
                spells.append(obj)
                off += self.get_struc_size(self.known_spell_desc)

            obj2 = {}
            self.read_struc (stream, off, self.spell_memorization_desc, obj2)

            self.abilities[key] = { 'spells': spells, 'memorization_info': obj2 }

        #self.read_list (stream, 'known_spell')
        #self.read_list (stream, 'spell_memorization')
        # effects
        self.read_list (stream, 'item')

        self.slots = {}
        self.read_struc (stream, self.header['item_slot_off'], self.item_slot_desc, self.slots)

    def printme (self):
        self.print_header ()

        for key in self.magic_class_keys:
            for i, spells in enumerate(self.known_spells[key]):
                self.print_list ("%s spell, lvl %d" %(key, i), self.known_spell_desc, spells['spells'])

        for key in range(1, 10):
            self.print_list ("Domain %d spell" %key, self.known_spell_desc, self.domain_spells[key]['spells'])

        for key in ('ability', 'song', 'shape'):
            self.print_list ("%s spell" %key, self.known_spell_desc, self.abilities[key]['spells'])

        #self.print_list ('spell_memorization')
        self.print_list ('item')

        self.print_struc (self.slots, self.item_slot_desc)


register_format (CRE_V22_Format, signature='CRE V2.2')
