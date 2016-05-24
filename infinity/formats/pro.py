# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2011 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

# Conforms to
#   IELister 40d421d0c87c570434ae5e46f4ea60703ac70671
#   IESDP 2011-03-15 (more or less)
#   GemRB 791fc422b23fa508588e9d616f78df8c5a6f655f

from infinity import core
from infinity.format import Format, register_format


class PRO_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'projectile_type',
              'type': 'WORD',
              'off': 0x0008,
              'enum': {1: 'no BAM',
                       2: 'single target',
                       3: 'aoe target' },
              'label': 'Projectile type' },

            { 'key': 'speed',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Speed' },


            { 'key': 'sparking_flag',
              'type': 'DWORD',
              'off': 0x000C,
              'mask': {0x01: 'sparks',
                       0x02: 'use z coordinate',
                       0x04: 'loop sound',
                       0x08: 'loop sound2',
                       0x10: 'do not affect direct target',
                       0x20: 'draw below animate objects' },
              'label': 'Sparking flag'},

            { 'key': 'wavc',
              'type': 'RESREF',
              'off': 0x0010,
              'label': 'WAVC resref'},

            { 'key': 'explosion_wavc',
              'type': 'RESREF',
              'off': 0x0018,
              'label': 'Explosion WAVC resref'},

            { 'key': 'unknown_wavc',
              'type': 'RESREF',
              'off': 0x0020,
              'label': 'Unknown/Unused? WAVC resref'},

            { 'key': 'spark_color',
              'type': 'DWORD',
              'off': 0x0028,
              'enum': 'SPRKCLR',
              'label': 'Spark color'},

            { 'key': 'gemrb_flags',
              'type': 'DWORD',
              'off': 0x002C,
              'mask': {0x00000001: 'bounce',
                       0x00000002: 'continue',
                       0x00000004: 'freeze',
                       0x00000008: 'no travel',
                       0x00000010: 'trail',
                       0x00000020: 'curved path',
                       0x00000040: 'random starting frame',
                       0x00000080: 'pile cycles',
                       0x00000100: 'half transparent',
                       0x00000200: 'tint',
                       0x00000400: 'iteration',
                       0x00000800: 'tiled',
                       0x00001000: 'falling',
                       0x00002000: 'incoming',
                       0x00004000: 'line',
                       0x00008000: 'wall',
                       0x00010000: 'draw under target',
                       0x00020000: 'pop',
                       0x00040000: 'unpop',
                       0x00080000: 'fade',
                       0x00100000: 'has setup text',
                       0x00200000: 'wandering',
                       0x00400000: 'random cycle',
                       0x00800000: 'rgb',
                       0x01000000: 'touch attack',
                       0x02000000: 'notids',
                       0x04000000: 'notids2',
                       0x08000000: 'both ids',
                       0x10000000: 'delay payload',
                       },
              'label': 'GemRB flags'},

            { 'key': 'gemrb_string_reference',
              'type': 'DWORD',
              'off': 0x0030,
              'label': 'GemRB String reference'},

            { 'key': 'gemrb_color',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'GemRB Color'},

            { 'key': 'gemrb_color_speed',
              'type': 'WORD',
              'off': 0x0038,
              'label': 'GemRB Color speed'},

            { 'key': 'gemrb_shake',
              'type': 'WORD',
              'off': 0x003A,
              'label': 'GemRB Shake'},

            { 'key': 'gemrb_ids_value',
              'type': 'WORD',
              'off': 0x003C,
              'label': 'GemRB IDS value'},

            { 'key': 'gemrb_ids_type',
              'type': 'WORD',
              'off': 0x003E,
              'label': 'GemRB IDS type'},

            { 'key': 'gemrb_ids_value_2',
              'type': 'WORD',
              'off': 0x0040,
              'label': 'GemRB IDS value 2'},

            { 'key': 'gemrb_ids_type_2',
              'type': 'WORD',
              'off': 0x0042,
              'label': 'GemRB IDS type 2'},

            { 'key': 'gemrb_fail_spell',
              'type': 'RESREF',
              'off': 0x0044,
              'label': 'GemRB Fail spell resref'},

            { 'key': 'gemrb_success_spell',
              'type': 'RESREF',
              'off': 0x004C,
              'label': 'GemRB Success spell resref'},

            { 'key': 'unknown54',
              'type': 'BYTES',
              'off': 0x0054,
              'size': 172,
              'label': 'Unknown 54'},

            { 'type': '_LABEL',
              'label': '\nTravel section:'},

            { 'type': '_INDENT',
              'label': '    '},

            { 'key': 'travel_flags',
              'type': 'DWORD',
              'off': 0x0100,
              'mask': {0x0001: 'fake BAM colors',
                       0x0002: 'has smoke',
                       0x0004: 'unknown bit 2',
                       0x0008: 'use area lighting',
                       0x0010: 'use area height',
                       0x0020: 'has shadow',
                       0x0040: 'has light spot',
                       0x0080: 'has brighten flags',
                       0x0100: 'low level brighten',
                       0x0200: 'high level brighten' },
              'label': 'Travel flags'},

            { 'key': 'travel_bam',
              'type': 'RESREF',
              'off': 0x0104,
              'label': 'BAM for travelling projectile'},

            { 'key': 'shadow_bam',
              'type': 'RESREF',
              'off': 0x010C,
              'label': 'BAM for projectile shadow'},

            { 'key': 'travel_cycle',
              'type': 'BYTE',
              'off': 0x0114,
              'label': 'BAM cycle for main projectile'},

            { 'key': 'shadow_bam_cycle',
              'type': 'BYTE',
              'off': 0x0115,
              'label': 'BAM cycle for projectile shadow'},

            { 'key': 'light_spot_intensity',
              'type': 'WORD',
              'off': 0x0116,
              'label': 'Light spot intensity'},

            { 'key': 'light_spot_size',
              'type': 'POINT',
              'off': 0x0118,
              'label': 'Light spot size'},

            { 'key': 'palette',
              'type': 'RESREF',
              'off': 0x011C,
              'label': 'Palette BMP'},

            { 'key': 'projectile_color',
              'type': 'BYTE',
              'off': 0x0124,
              'count': 7,
              'label': 'Projectile color'},

            { 'type': '_DEDENT',
              'label': ''},

            { 'type': '_LABEL',
              'label': '\nSmoke section:'},

            { 'type': '_INDENT',
              'label': '    '},

            { 'key': 'smoke_puff_frequency',
              'type': 'BYTE',
              'off': 0x012B,
              'label': 'Smoke puff frequency'},

            { 'key': 'smoke_puff_color',
              'type': 'BYTE',
              'off': 0x012C,
              'count': 7,
              'label': 'Smoke puff color'},

            { 'key': 'face_target',
              'type': 'BYTE',
              'off': 0x0133,
              'enum': {1: 'dont face',
                       5: 'mirrored eastern direction (reduced granularity)',
                       9: 'reduced eastern direction (full granularity)',
                       16: 'not mirrored, not reduced' },
              'label': 'Face target'},

            { 'key': 'smoke_animation',
              'type': 'WORD',
              'off': 0x0134,
              'enum': 'ANIMATE',
              'label': 'Smoke reference to ANIMATE.IDS'},

            { 'key': 'secondary_missile_bam',
              'type': 'RESREF',
              'off': 0x0136,
              'label': 'BAM for secondary missiles'},

            { 'key': 'tertiary_missile_bam',
              'type': 'RESREF',
              'off': 0x013E,
              'label': 'BAM for tertiary missiles'},

            { 'key': 'quarternary_missile_bam',
              'type': 'RESREF',
              'off': 0x0146,
              'label': 'BAM for quarternary missiles'},

            { 'key': 'secondary_missile_frequency',
              'type': 'WORD',
              'off': 0x014E,
              'label': 'Frequency of secondary missiles'},

            { 'key': 'tertiary_missile_frequency',
              'type': 'WORD',
              'off': 0x0150,
              'label': 'Frequency of tertiary missiles'},

            { 'key': 'quarternary_missile_frequency',
              'type': 'WORD',
              'off': 0x0152,
              'label': 'Frequency of quarternary missiles'},

            { 'key': 'unknown154',
              'type': 'BYTES',
              'off': 0x0154,
              'size': 172, # FIXME: IESDP has wrongly 176 here
              'label': 'Unknown 154'},

            { 'type': '_DEDENT',
              'label': ''},

            )

    aoe_header_desc = (
            { 'type': '_LABEL',
              'label': '\nAOE section:'},

            { 'type': '_INDENT',
              'label': '    '},

            { 'key': 'aoe_flags',
              'type': 'DWORD',
              'off': 0x0200,
              'mask': {0x0001: 'stay visible at destination',
                       0x0002: 'triggered by inanimate objects',
                       0x0004: 'triggered on condition',
                       0x0008: 'trigger during delay',
                       0x0010: 'use secondary projectile',
                       0x0020: 'draw fragments',
                       0x0040: 'target party or not party',
                       0x0080: 'target party',
                       0x0100: 'num of triggers eq to mage caster level',
                       0x0200: 'num of triggers eq to cleric caster level',
                       0x0400: 'use VVC',
                       0x0800: 'cone shape',
                       0x1000: 'ignore obstacles',
                       0x2000: 'check triggers from anim frame 30',
                       0x4000: 'delayed explosion',
                       0x8000: 'affect only one' },
              'label': 'AOE target (enemies/allies)'},

            { 'key': 'trigger_radius',
              'type': 'WORD',
              'off': 0x0204,
              'label': 'Trigger radius'},

            { 'key': 'effect_radius',
              'type': 'WORD',
              'off': 0x0206,
              'label': 'Effect radius'},

            { 'key': 'trigger_sound',
              'type': 'RESREF',
              'off': 0x0208,
              'label': 'Trigger sound'},

            { 'key': 'delay_between_explosions',
              'type': 'WORD',
              'off': 0x0210,
              'label': 'Delay between explosions'},

            { 'key': 'explosion_fragments',
              'type': 'WORD',
              'off': 0x0212,
              'enum': 'ANIMATE',
              'label': 'Explosion fragments to ANIMATE.IDS'},

            { 'key': 'secondary_projectile',
              'type': 'WORD',
              'off': 0x0214,
              'enum': 'PROJECTL',
              'label': 'Secondary projectile PROJECTL-1'},

            { 'key': 'trigger_count',
              'type': 'BYTE',
              'off': 0x0216,
              'label': 'Duration/Trigger count'},

            { 'key': '1st_explosion_projectile',
              'type': 'BYTE',
              'off': 0x0217,
              'enum': 'FIREBALL',
              'label': '1st explosion projectile ref to FIREBALL.IDS'},

            { 'key': '1st_explosion_color',
              'type': 'WORD',
              'off': 0x0218,
              'label': '1st explosion color'},

            { 'key': 'explosion_projectile',
              'type': 'WORD',
              'off': 0x021A,
              'enum': 'PROJECTL',
              'label': 'Explosion projectile ref to PROJECTL.IDS'},

            { 'key': 'vvc',
              'type': 'RESREF',
              'off': 0x021C,
              'label': 'Explosion animation VVC'},

            { 'key': 'cone_width',
              'type': 'WORD',
              'off': 0x0224,
              'label': 'Cone width'},

            { 'key': 'unknown226',
              'type': 'WORD',
              'off': 0x0226,
              'label': 'Unknown 226'},

            { 'key': 'gemrb_spread_animation',
              'type': 'RESREF',
              'off': 0x0228,
              'label': 'GemRB Spread animation'},

            { 'key': 'gemrb_secondary_animation',
              'type': 'RESREF',
              'off': 0x0230,
              'label': 'GemRB Secondary animation'},

            { 'key': 'gemrb_area_sound',
              'type': 'RESREF',
              'off': 0x0238,
              'label': 'GemRB Area sound'},

            { 'key': 'gemrb_aoe_flags',
              'type': 'DWORD',
              'off': 0x0240,
              'mask': {0x00000001: 'tint',
                       0x00000002: 'fill',
                       0x00000004: 'scatter',
                       0x00000008: 'vvcpal',
                       0x00000010: 'spread',
                       0x00000020: 'palette',
                       0x00000040: 'both anims',
                       0x00000080: 'more children',
                       0x00000100: 'spellfail',
                       0x00000200: 'multi directional',
                       0x00000400: 'target hd',
                       0x00000800: 'invert target' },
              'label': 'GemRB AoE flags'},

            { 'key': 'gemrb_dice_count',
              'type': 'WORD',
              'off': 0x0244,
              'label': 'GemRB Dice count'},

            { 'key': 'gemrb_dice_sides',
              'type': 'WORD',
              'off': 0x0246,
              'label': 'GemRB Dice sides'},

            { 'key': 'unknown248',
              'type': 'BYTES',
              'off': 0x0248,
              'size': 184,
              'label': 'Unknown 248'},

            { 'type': '_DEDENT',
              'label': ''},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'PRO'


    def read (self, stream):
        self.read_header (stream)
        if self.header['projectile_type'] == 3:
            self.read_struc (stream, 0x0000, self.aoe_header_desc, self.header)


    def write (self, stream):
        self.write_header (stream)
        if self.header['projectile_type'] == 3:
            self.write_struc (stream, 0x0000, self.aoe_header_desc, self.header)


    def printme (self):
        self.print_header ()
        if self.header['projectile_type'] == 3:
            self.print_struc (self.header, self.aoe_header_desc)



register_format (PRO_Format, signature='PRO V1.0', extension='PRO', name=('PRO', 'PROJECTILE'), type=0x3fd)
