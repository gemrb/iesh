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


class CRE_V12_Format (Format):

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
              'mask': { 0x0001: 'Dmg doesn\'t stop casting', 0x0002: 'No corpse', 0x0004: 'Keep corpse', 0x0008: 'Orig class Fighter', 0x0010: 'Orig class Mage', 0x0020: 'Orig class Cleric', 0x0040: 'Orig class Thief', 0x0080: 'Orig class Druid', 0x0100: 'Orig class Ranger', 0x0200: 'Fallen Paladin', 0x0400: 'Fallen Ranger', 0x0800: 'Exportable', 0x1000: 'Unknown bit12', 0x2000: 'Unknown bit13', 0x4000: 'Can activate non-NPC triggers?', 0x8000: 'Been in party'},
              'label': 'Creature flags'},

            { 'key': 'xp',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'XP'},

            { 'key': 'power_level',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Creature power level'},

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
              'type': 'WORD',
              'off': 0x0028,
              'enum': 'ANIMATE',
              'label': 'Animation ID'},  # as per ANIMATE.IDS

            { 'key': 'unknown_2A',
                'type': 'WORD',
                'off': 0x002A,
                'label': 'Unknown 2A' },

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

            { 'key': 'armor_class_natural',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x0046,
                'label': 'Armor class (natural)' },

            { 'key': 'armor_class_effective',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x0048,
                'label': 'Armor class (effective)' },

            { 'key': 'armor_class_crushing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004A,
                'label': 'Armor class (crushing att mod)' },

            { 'key': 'armor_class_missile_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004C,
                'label': 'Armor class (missile att mod)' },

            { 'key': 'armor_class_piercing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x004E,
                'label': 'Armor class (piercing att mod)' },

            { 'key': 'armor_class_slashing_mod',
                'type': 'WORD',  # FIXME: actually signed word
                'off': 0x0050,
                'label': 'Armor class (slashing att mod)' },

            { 'key': 'thac0',
                'type': 'BYTE',
                'off': 0x0052,
                'label': 'THAC0 (1-25)' },

            { 'key': 'num_attacks',
                'type': 'BYTE',
                'off': 0x0053,
                'label': 'Number of attacks (0-10)' },

            { 'key': 'save_vs_death',
                'type': 'BYTE',
                'off': 0x0054,
                'label': 'Save versus death (0-20)' },

            { 'key': 'save_vs_wands',
                'type': 'BYTE',
                'off': 0x0055,
                'label': 'Save versus wands (0-20)' },

            { 'key': 'save_vs_polymorph',
                'type': 'BYTE',
                'off': 0x0056,
                'label': 'Save versus polymorph (0-20)' },

            { 'key': 'save_vs_breath',
                'type': 'BYTE',
                'off': 0x0057,
                'label': 'Save versus breath attacks (0-20)' },

            { 'key': 'save_vs_spells',
                'type': 'BYTE',
                'off': 0x0058,
                'label': 'Save versus spells (0-20)' },

            { 'key': 'resist_fire',
                'type': 'BYTE',
                'off': 0x0059,
                'label': 'Resist fire (0-100)' },

            { 'key': 'resist_cold',
                'type': 'BYTE',
                'off': 0x005A,
                'label': 'Resist cold (0-100)' },

            { 'key': 'resist_electricity',
                'type': 'BYTE',
                'off': 0x005B,
                'label': 'Resist electricity (0-100)' },

            { 'key': 'resist_acid',
                'type': 'BYTE',
                'off': 0x005C,
                'label': 'Resist acid (0-100)' },

            { 'key': 'resist_magic',
                'type': 'BYTE',
                'off': 0x005D,
                'label': 'Resist magic (0-100)' },

            { 'key': 'resist_magic_fire',
                'type': 'BYTE',
                'off': 0x005E,
                'label': 'Resist magic fire (0-100)' },

            { 'key': 'resist_magic_cold',
                'type': 'BYTE',
                'off': 0x005F,
                'label': 'Resist magic cold (0-100)' },

            { 'key': 'resist_slashing',
                'type': 'BYTE',
                'off': 0x0060,
                'label': 'Resist slashing (0-100)' },

            { 'key': 'resist_crushing',
                'type': 'BYTE',
                'off': 0x0061,
                'label': 'Resist crushing (0-100)' },

            { 'key': 'resist_piercing',
                'type': 'BYTE',
                'off': 0x0062,
                'label': 'Resist piercing (0-100)' },

            { 'key': 'resist_missile',
                'type': 'BYTE',
                'off': 0x0063,
                'label': 'Resist missile (0-100)' },

            { 'key': 'detect_illusion',
                'type': 'BYTE',
                'off': 0x0064,
                'label': 'Detect illusion' },

            { 'key': 'set_traps',
                'type': 'BYTE',
                'off': 0x0065,
                'label': 'Set traps' },

            { 'key': 'lore',
                'type': 'BYTE',
                'off': 0x0066,
                'label': 'Lore' },

            { 'key': 'lockpicking',
                'type': 'BYTE',
                'off': 0x0067,
                'label': 'Lockpicking' },

            { 'key': 'stealth',
                'type': 'BYTE',
                'off': 0x0068,
                'label': 'Stealth' },

            { 'key': 'find_disarm_traps',
                'type': 'BYTE',
                'off': 0x0069,
                'label': 'Find and disarm traps' },

            { 'key': 'pick_pockets',
                'type': 'BYTE',
                'off': 0x006A,
                'label': 'Pick pockets' },

            { 'key': 'fatigue',
                'type': 'BYTE',
                'off': 0x006B,
                'label': 'Fatigue' },

            { 'key': 'intoxication',
                'type': 'BYTE',
                'off': 0x006C,
                'label': 'Intoxication' },

            { 'key': 'luck',
                'type': 'BYTE',
                'off': 0x006D,
                'label': 'Luck' },

            { 'key': 'fist_proficiency',
                'type': 'BYTE',
                'off': 0x006E,
                'label': 'Fist proficiency' },

            { 'key': 'edged_proficiency',
                'type': 'BYTE',
                'off': 0x006F,
                'label': 'Edged proficiency' },

            { 'key': 'hammer_proficiency',
                'type': 'BYTE',
                'off': 0x0070,
                'label': 'Hammer proficiency' },

            { 'key': 'axe_proficiency',
                'type': 'BYTE',
                'off': 0x0071,
                'label': 'Axe proficiency' },

            { 'key': 'club_proficiency',
                'type': 'BYTE',
                'off': 0x0072,
                'label': 'Club proficiency' },

            { 'key': 'bow_proficiency',
                'type': 'BYTE',
                'off': 0x0073,
                'label': 'Bow proficiency' },

            { 'key': 'unused_proficiency',
                'type': 'BYTE',
                'off': 0x0074,
                'count': 15,
                'label': 'Unused proficiency slot' },

            { 'key': 'tracking_skill',
                'type': 'BYTE',
                'off': 0x0083,
                'label': 'Tracking skill' },

            { 'key': 'unknown_84',
                'type': 'BYTES',
                'off': 0x0084,
                'size': 32,
                'label': 'Unknown 84' },


            { 'key': 'strref',      # see SOUNDOFF.IDS (for BG1) and SNDSLOT.IDS for (BG2)
                'type': 'STRREF',
                'off': 0x00A4,
                'count': 100,
                'label': 'Strref' },

            { 'key': 'primary_highest_level',
                'type': 'BYTE',
                'off': 0x0234,
                'label': 'Highest level in primary class' },

            { 'key': 'secondary_highest_level',
                'type': 'BYTE',
                'off': 0x0235,
                'label': 'Highest level in secondary class' },

            { 'key': 'tertiary_highest_level',
                'type': 'BYTE',
                'off': 0x0236,
                'label': 'Highest level in tertiary class' },

            { 'key': 'sex',
                'type': 'BYTE',
                'off': 0x0237,
                'enum': 'gender',
                'label': 'Sex (not modified)' },

            { 'key': 'strength',
                'type': 'BYTE',
                'off': 0x0238,
                'label': 'Strength' },

            { 'key': 'strength_bonus',
                'type': 'BYTE',
                'off': 0x0239,
                'label': 'Strength % bonus' },

            { 'key': 'intelligence',
                'type': 'BYTE',
                'off': 0x023A,
                'label': 'Intelligence' },

            { 'key': 'wisdom',
                'type': 'BYTE',
                'off': 0x023B,
                'label': 'Wisdom' },

            { 'key': 'dexterity',
                'type': 'BYTE',
                'off': 0x023C,
                'label': 'Dexterity' },

            { 'key': 'constitution',
                'type': 'BYTE',
                'off': 0x023D,
                'label': 'Constitution' },

            { 'key': 'charisma',
                'type': 'BYTE',
                'off': 0x023E,
                'label': 'Charisma' },

            { 'key': 'morale',
                'type': 'BYTE',
                'off': 0x023F,
                'label': 'Morale' },

            { 'key': 'morale_break',
                'type': 'BYTE',
                'off': 0x0240,
                'label': 'Morale break' },

            { 'key': 'racial_enemy',
                'type': 'BYTE',
                'off': 0x0241,
                'enum': 'race',
                'label': 'Racial enemy' },

            { 'key': 'morale_recovery_time',
                'type': 'BYTE',
                'off': 0x0242,
                'label': 'Morale recovery time' },

            { 'key': 'unknown_243',
                'type': 'BYTE',
                'off': 0x0243,
                'label': 'Unknown 243' },

            { 'key': 'kit_info',
                'type': 'DWORD',
                'off': 0x0244,
                'mask': { 0x00000000: 'None', 0x00400000: 'Abjurer', 0x00800000: 'Conjurer', 0x01000000: 'Diviner', 0x02000000: 'Enchanter', 0x04000000: 'Illusionist', 0x08000000: 'Invoker', 0x10000000: 'Necromancer', 0x20000000: 'Transmuter' },
                'label': 'Kit information' },

            { 'key': 'override_script',
                'type': 'RESREF',
                'off': 0x0248,
                'label': 'Creature script - override' },

            { 'key': 'class_script',
                'type': 'RESREF',
                'off': 0x0250,
                'label': 'Creature script - class' },

            { 'key': 'race_script',
                'type': 'RESREF',
                'off': 0x0258,
                'label': 'Creature script - race' },

            { 'key': 'general_script',
                'type': 'RESREF',
                'off': 0x0260,
                'label': 'Creature script - general' },

            { 'key': 'default_script',
                'type': 'RESREF',
                'off': 0x0268,
                'label': 'Creature script - default' },

            { 'key': 'unknown_270',
                'type': 'BYTES',
                'off': 0x0270,
                'size': 36,
                'label': 'Unknown 270' },

            { 'key': 'overlay_off',
                'type': 'DWORD',
                'off': 0x0294,
                'label': 'Offset to overlay section' },

            { 'key': 'overlay_cnt',
                'type': 'DWORD',
                'off': 0x0298,
                'label': 'Size of overlay section' },

            { 'key': 'xp_secondary',
                'type': 'DWORD',
                'off': 0x029C,
                'label': 'XP (secondary class)' },

            { 'key': 'xp_tertiary',
                'type': 'DWORD',
                'off': 0x02A0,
                'label': 'XP (tertiary class)' },

            { 'key': 'internal',
                'type': 'WORD',
                'off': 0x02A4,
                'count': 12, # FIXME: IESDP has 10 here
                'label': 'Internal' },

            { 'key': 'monstrous_compendium_entry',
                'type': 'STR32',
                'off': 0x02BC,  # FIXME: IESDP has 2B8 here
                'label': 'Monstrous compendium entry' },

            { 'key': 'dialog_activation_range',
                'type': 'BYTE',
                'off': 0x02DC,
                'label': 'Dialog activation range' },

            { 'key': 'selection_cirle_size',
                'type': 'BYTE',
                'off': 0x02DD,
                'label': 'Selection circle size' },

            { 'key': 'unknown_2DE',
                'type': 'BYTE',
                'off': 0x002DE,
                'label': 'Unknown 2DE' },

            { 'key': 'num_colors',
                'type': 'BYTE',
                'off': 0x02DF,
                'label': 'Number of colors' },

            { 'key': 'attr_flags',
                'type': 'DWORD',
                'off': 0x02E0,
                'mask': { 0x0002: 'Transparent', 0x100: 'Invulnerable' },
                'label': 'Attribute flags' },

            { 'key': 'color',
                'type': 'WORD',
                'off': 0x02E4,
                'enum': 'Clownclr',
                'count': 7,
                'label': 'Color' },

            { 'key': 'unknown_2F2',
                'type': 'BYTES',
                'off': 0x002F2,
                'size': 3,
                'label': 'Unknown 2F2' },

            { 'key': 'color_placement',
                'type': 'BYTE',
                'off': 0x02F5,
                'count': 7,
                'label': 'Color placement' },

            { 'key': 'unknown_2FC',
                'type': 'BYTES',
                'off': 0x002FC,
                'size': 21,
                'label': 'Unknown 2FC' },

            { 'key': 'species',
                'type': 'BYTE',
                'off': 0x0311,
                'enum': 'RACE',
                'label': 'Species' },

            { 'key': 'team',
                'type': 'BYTE',
                'off': 0x0312,
                'enum': 'TEAM',
                'label': 'Team' },

            { 'key': 'faction',
                'type': 'BYTE',
                'off': 0x0313,
                'enum': 'FACTION',
                'label': 'Faction' },

            { 'key': 'enemy_ally',
                'type': 'BYTE',
                'off': 0x0314,
                'enum': 'EA',
                'label': 'Enemy-Ally' },

            { 'key': 'general',
                'type': 'BYTE',
                'off': 0x0315,
                'enum': 'GENERAL',
                'label': 'General' },

            { 'key': 'race',
                'type': 'BYTE',
                'off': 0x0316,
                'enum': 'RACE',
                'label': 'Race' },

            { 'key': 'class',
                'type': 'BYTE',
                'off': 0x0317,
                'enum': 'CLASS',
                'label': 'Class' },

            { 'key': 'specific',
                'type': 'BYTE',
                'off': 0x0318,
                'enum': 'SPECIFIC',
                'label': 'Specific' },

            { 'key': 'gender',
                'type': 'BYTE',
                'off': 0x0319,
                'enum': 'GENDER',
                'label': 'Gender' },

            { 'key': 'unknown_31A',
                'type': 'BYTES',
                'off': 0x031A,
                'size': 5,
                'label': 'Unknown 31A' },

            { 'key': 'alignment',
                'type': 'BYTE',
                'off': 0x031F,
                'enum': 'ALIGNMEN',
                'label': 'Alignment' },

            { 'key': 'global_actor_enumeration',
                'type': 'WORD',
                'off': 0x0320,
                'label': 'Global actor enumeration value' },

            { 'key': 'local_actor_enumeration',
                'type': 'WORD',
                'off': 0x0322,
                'label': 'Local (area) actor enumeration value' },

            { 'key': 'death_var',
                'type': 'STR32',
                'off': 0x0324,
                'label': 'Death variable' },

            { 'key': 'known_spell_off',
                'type': 'DWORD',
                'off': 0x0344,
                'label': 'Offset of known spells' },

            { 'key': 'known_spell_cnt',
                'type': 'DWORD',
                'off': 0x0348,
                'label': 'Count of known spells' },

            { 'key': 'spell_memorization_off',
                'type': 'DWORD',
                'off': 0x034C,
                'label': 'Offset of spell memorization infos' },

            { 'key': 'spell_memorization_cnt',
                'type': 'DWORD',
                'off': 0x0350,
                'label': 'Count of spell memorization infos' },

            { 'key': 'memorized_spell_off',
                'type': 'DWORD',
                'off': 0x0354,
                'label': 'Offset of memorized spells' },

            { 'key': 'memorized_spell_cnt',
                'type': 'DWORD',
                'off': 0x0358,
                'label': 'Count of memorized spells' },

            { 'key': 'item_slot_off',
                'type': 'DWORD',
                'off': 0x035C,
                'label': 'Offset of items slots' },

            { 'key': 'item_off',
                'type': 'DWORD',
                'off': 0x0360,
                'label': 'Offset of items' },

            { 'key': 'item_cnt',
                'type': 'DWORD',
                'off': 0x0364,
                'label': 'Count of items' },

            { 'key': 'effect_off',
                'type': 'DWORD',
                'off': 0x0368,
                'label': 'Offset of effects' },

            { 'key': 'effect_cnt',
                'type': 'DWORD',
                'off': 0x036C,
                'label': 'Count of effects' },

            { 'key': 'dialog',
                'type': 'RESREF',
                'off': 0x0370,
                'label': 'Dialog resref' },
            )

    overlay_desc = (
            { 'key': 'unknown_00',
                'type': 'BYTES',
                'off': 0x0000,
                'size': 36,
                'label': 'Unknown 00' },
            )

    known_spell_desc = (
            { 'key': 'resref',
                'type': 'RESREF',
                'restype': 'SPL',
                'off': 0x0000,
                'label': 'SPL resref' },

            { 'key': 'level',
                'type': 'WORD',
                'off': 0x0008,
                'label': 'Spell level -1' },

            { 'key': 'type',
                'type': 'WORD',
                'off': 0x000A,
                'enum': { 0: 'Priest', 1: 'Wizard', 2: 'Innate' },
                'label': 'Spell type' },
            )

    spell_memorization_desc = (
            { 'key': 'level',
                'type': 'WORD',
                'off': 0x0000,
                'label': 'Spell level -1' },

            { 'key': 'num_memorizable',
                'type': 'WORD',
                'off': 0x0002,
                'label': 'Number of spells memorizable' },

            { 'key': 'num_memorizable_after_fx',
                'type': 'WORD',
                'off': 0x0004,
                'label': 'Number of spells memorizable after effects' },

            { 'key': 'type',
                'type': 'WORD',
                'off': 0x0006,
                'enum': { 0: 'Priest', 1: 'Wizard', 2: 'Innate' },
                'label': 'Spell type' },

            { 'key': 'memorized_spell_ndx',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Index to memorized spells' },

            { 'key': 'memorized_spell_cnt',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Count of memorized spells' },
            )

    memorized_spell_desc = (
            { 'key': 'resref',
                'type': 'RESREF',
                'restype': 'SPL',
                'off': 0x0000,
                'label': 'SPL resref' },

            { 'key': 'memorized',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Memorized' },
    )


    item_desc = (
            { 'key': 'item_resref',
                'type': 'RESREF',
                'restype': 'ITM',
                'off': 0x0000,
                'label': 'ITM resref' },

            { 'key': 'unknown_08',
                'type': 'WORD',
                'off': 0x0008,
                'label': 'Unknown 08' },

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
                'mask': { 0x01: 'Identified', 0x02: 'Unstealable', 0x04: 'Stolen', 0x08: 'Undroppable' },
                'label': 'Flags' },
    )

    item_slot_desc = (
            { 'key': 'item',
                'type': 'WORD',
                'off': 0x0000,
                'count': 46,
                'label': 'Item' },

            { 'key': 'selected_weapon', # IESDP: Values are from slots.ids - 35, with 1000 meaning "fist".
                'type': 'WORD',
                'off': 0x005C,
                'label': 'Selected Weapon' },

            { 'key': 'selected_weapon_ability',
                'type': 'WORD',
                'off': 0x005E,
                'label': 'Selected Weapon Ability' },
    )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'CRE'

        self.overlay_list = []
        self.known_spell_list = []
        self.spell_memorization_list = []
        self.item_list = []
        self.memorized_spell_list = []
        self.slots = None

    def read (self, stream):
        self.read_header (stream)
        self.read_list (stream, 'overlay')
        self.read_list (stream, 'known_spell')
        self.read_list (stream, 'spell_memorization')
        self.read_list (stream, 'memorized_spell')
        self.read_list (stream, 'item')

        self.slots = {}
        self.read_struc (stream, self.header['item_slot_off'], self.item_slot_desc, self.slots)

    def printme (self):
        self.print_header ()
        self.print_list ('known_spell')
        self.print_list ('overlay')
        self.print_list ('memorized_spell')
        self.print_list ('spell_memorization')
        self.print_list ('item')

        self.print_struc (self.slots, self.item_slot_desc)


class CRE_V11_Format (CRE_V12_Format):
    item_slot_desc = (
            { 'key': 'item',
                'type': 'WORD',
                'off': 0x0000,
                'count': 38,
                'label': 'Item' },

            { 'key': 'selected_weapon', # IESDP: Values are from slots.ids - 35, with 1000 meaning "fist".
                'type': 'WORD',
                'off': 0x004C,
                'label': 'Selected Weapon' },

            { 'key': 'selected_weapon_ability',
                'type': 'WORD',
                'off': 0x004E,
                'label': 'Selected Weapon Ability' },
    )

register_format ('CRE', 'V1.2', CRE_V12_Format)
register_format ('CRE', 'V1.1', CRE_V11_Format)
