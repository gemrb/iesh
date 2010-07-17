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


class CRE_V90_Format (Format):

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
              'mask': { 0x0001: 'Dmg doesn\'t stop casting', 0x0002: 'No corpse', 0x0004: 'Keep corpse', 0x0008: 'Orig class Fighter', 0x0010: 'Orig class Mage', 0x0020: 'Orig class Cleric', 0x0040: 'Orig class Thief', 0x0080: 'Orig class Druid', 0x0100: 'Orig class Ranger', 0x0200: 'Fallen Paladin', 0x0400: 'Fallen Ranger', 0x0800: 'Exportable', 0x1000: 'Unknown bit12', 0x2000: 'Unknown bit13', 0x4000: 'Can activate non-NPC triggers?', 0x8000: 'Been in party' },
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

            { 'key': 'large_sword_proficiency',
                'type': 'BYTE',
                'off': 0x006E,
                'label': 'Large sword proficiency' },

            { 'key': 'small_sword_proficiency',
                'type': 'BYTE',
                'off': 0x006F,
                'label': 'Small sword proficiency' },

            { 'key': 'bow_proficiency',
                'type': 'BYTE',
                'off': 0x0070,
                'label': 'Bow proficiency' },

            { 'key': 'spear_proficiency',
                'type': 'BYTE',
                'off': 0x0071,
                'label': 'Spear proficiency' },

            { 'key': 'axe_proficiency',
                'type': 'BYTE',
                'off': 0x0072,
                'label': 'Axe proficiency' },

            { 'key': 'missile_proficiency',
                'type': 'BYTE',
                'off': 0x0073,
                'label': 'Missile proficiency' },

            { 'key': 'great_sword_proficiency',
                'type': 'BYTE',
                'off': 0x0074,
                'label': 'Great sword proficiency' },

            { 'key': 'dagger_proficiency',
                'type': 'BYTE',
                'off': 0x0075,
                'label': 'Dagger proficiency' },

            { 'key': 'halberd_proficiency',
                'type': 'BYTE',
                'off': 0x0076,
                'label': 'Halberd proficiency' },

            { 'key': 'mace_proficiency',
                'type': 'BYTE',
                'off': 0x0077,
                'label': 'Mace proficiency' },

            { 'key': 'flail_proficiency',
                'type': 'BYTE',
                'off': 0x0078,
                'label': 'Flail proficiency' },

            { 'key': 'hammer_proficiency',
                'type': 'BYTE',
                'off': 0x0079,
                'label': 'Hammer proficiency' },

            { 'key': 'club_proficiency',
                'type': 'BYTE',
                'off': 0x007A,
                'label': 'Club proficiency' },

            { 'key': 'quarterstaff_proficiency',
                'type': 'BYTE',
                'off': 0x007B,
                'label': 'Quarterstaff proficiency' },

            { 'key': 'crossbow_proficiency',
                'type': 'BYTE',
                'off': 0x007C,
                'label': 'Crossbow proficiency' },

            { 'key': 'unknown_7d',
                'type': 'BYTES',
                'off': 0x007d,
                'size': 6,
                'label': 'Unknown 7D' },

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
                'mask': { 0x00000000: 'NONE', 0x00400000: 'ABJURER', 0x00800000: 'CONJURER', 0x01000000: 'DIVINER', 0x02000000: 'ENCHANTER', 0x04000000: 'ILLUSIONIST', 0x08000000: 'INVOKER', 0x10000000: 'NECROMANCER', 0x20000000: 'TRANSMUTER' },
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

            { 'key': 'visible',
                'type': 'BYTE',
                'off': 0x0270,
                'label': 'Visible' },

            { 'key': 'set_dead_var',
                'type': 'BYTE',
                'off': 0x0271,
                'label': 'Set _DEAD variable on death' },

            { 'key': 'set_kill_cnt_var',
                'type': 'BYTE',
                'off': 0x0272,
                'label': 'Set KILL_<scriptname>_CNT variable on death' },

            { 'key': 'unknown_273',
                'type': 'BYTE',
                'off': 0x0273,
                'label': 'Unknown 273' },

            { 'key': 'internal_variables',
                'type': 'WORD',
                'off': 0x0274,
                'count': 5,
                'label': 'Internal variables' },

            { 'key': 'secondary_death_var',
                'type': 'STR32',
                'off': 0x027E,
                'label': 'Secondary death variable' },

            { 'key': 'tertiary_death_var',
                'type': 'STR32',
                'off': 0x029E,
                'label': 'Tertiary death variable' },

            { 'key': 'unknown_2BE',
                'type': 'WORD',
                'off': 0x02BE,
                'label': 'Unknown 2BE' },

            { 'key': 'saved_x_coord',
                'type': 'WORD',
                'off': 0x02C0,
                'label': 'Saved X coord' },

            { 'key': 'saved_y_coord',
                'type': 'WORD',
                'off': 0x02C2,
                'label': 'Saved Y coord' },

            { 'key': 'saved_orientation',
                'type': 'WORD',
                'off': 0x02C4,
                'label': 'Saved orientation' },

            { 'key': 'unknown_2C6',
                'type': 'BYTES',
                'off': 0x02C6,
                'size': 18,
                'label': 'Unknown 2C6' },

            { 'key': 'enemy_ally',
                'type': 'BYTE',
                'off': 0x02D8,
                'enum': 'EA',
                'label': 'Enemy-Ally' },

            { 'key': 'general',
                'type': 'BYTE',
                'off': 0x02D9,
                'enum': 'GENERAL',
                'label': 'General' },

            { 'key': 'race',
                'type': 'BYTE',
                'off': 0x02DA,
                'enum': 'RACE',
                'label': 'Race' },

            { 'key': 'class',
                'type': 'BYTE',
                'off': 0x02DB,
                'enum': 'CLASS',
                'label': 'Class' },

            { 'key': 'specific',
                'type': 'BYTE',
                'off': 0x02DC,
                'enum': 'SPECIFIC',
                'label': 'Specific' },

            { 'key': 'gender',
                'type': 'BYTE',
                'off': 0x02DD,
                'enum': 'GENDER',
                'label': 'Gender' },

            { 'key': 'unknown_2DE',
                'type': 'BYTES',
                'off': 0x02DE,
                'size': 5,
                'label': 'Unknown 2DE' },

            { 'key': 'alignment',
                'type': 'BYTE',
                'off': 0x02E3,
                'enum': 'ALIGNMEN',
                'label': 'Alignment' },

            { 'key': 'global_actor_enumeration',
                'type': 'WORD',
                'off': 0x02E4,
                'label': 'Global actor enumeration value' },

            { 'key': 'local_actor_enumeration',
                'type': 'WORD',
                'off': 0x02E6,
                'label': 'Local (area) actor enumeration value' },

            { 'key': 'death_var',
                'type': 'STR32',
                'off': 0x02E8,
                'label': 'Death variable' },

            { 'key': 'known_spell_off',
                'type': 'DWORD',
                'off': 0x0308,
                'label': 'Offset of known spells' },

            { 'key': 'known_spell_cnt',
                'type': 'DWORD',
                'off': 0x030C,
                'label': 'Count of known spells' },

            { 'key': 'spell_memorization_off',
                'type': 'DWORD',
                'off': 0x0310,
                'label': 'Offset of spell memorization infos' },

            { 'key': 'spell_memorization_cnt',
                'type': 'DWORD',
                'off': 0x0314,
                'label': 'Count of spell memorization infos' },

            { 'key': 'memorized_spell_off',
                'type': 'DWORD',
                'off': 0x0318,
                'label': 'Offset of memorized spells' },

            { 'key': 'memorized_spell_cnt',
                'type': 'DWORD',
                'off': 0x031C,
                'label': 'Count of memorized spells' },

            { 'key': 'item_slot_off',
                'type': 'DWORD',
                'off': 0x0320,
                'label': 'Offset of items slots' },

            { 'key': 'item_off',
                'type': 'DWORD',
                'off': 0x0324,
                'label': 'Offset of items' },

            { 'key': 'item_cnt',
                'type': 'DWORD',
                'off': 0x0328,
                'label': 'Count of items' },

            { 'key': 'effect_off',
                'type': 'DWORD',
                'off': 0x032C,
                'label': 'Offset of effects' },

            { 'key': 'effect_cnt',
                'type': 'DWORD',
                'off': 0x0330,
                'label': 'Count of effects' },

            { 'key': 'dialog',
                'type': 'RESREF',
                'restype': 'DLG',
                'off': 0x0334,
                'label': 'Dialog resref' },
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
                'mask': { 0x01: 'Identified', 0x02: 'Unstealable', 0x04: 'Stolen', 0x08: 'Magical' },
                'label': 'Flags' },
    )

    item_slot_desc = (
            { 'key': 'item',
                'type': 'WORD',
                'off': 0x0000,
                'count': 38,
                'label': 'Item' },

            { 'key': 'selected_weapon',
                'type': 'DWORD',
                'off': 0x004C,
                'enum': { 0: 'Weapon 1', 1: 'Weapon 2', 2: 'Weapon 3', 3: 'Weapon 4', 1000: 'No slot', 65512: 'Quiver 1', 65513: 'Quiver 2', 65514: 'Quiver 3' }, # FIXME: quivers are likely wrong
                'label': 'Selected Weapon' },

    )


    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'CRE'

        self.known_spell_list = []
        self.spell_memorization_list = []
        self.item_list = []
        self.memorized_spell_list = []
        self.slots = None
        self.selected = None


    def read (self, stream):
        self.read_header (stream)
        self.read_list (stream, 'known_spell')
        self.read_list (stream, 'spell_memorization')
        self.read_list (stream, 'memorized_spell')
        self.read_list (stream, 'item')

        self.slots = {}
        self.read_struc (stream, self.header['item_slot_off'], self.item_slot_desc, self.slots)


    def printme (self):
        self.print_header ()
        self.print_list ('known_spell')
        self.print_list ('memorized_spell')
        self.print_list ('spell_memorization')
        self.print_list ('item')

        self.print_struc (self.slots, self.item_slot_desc)



register_format ('CRE', 'V9.0', CRE_V90_Format)
