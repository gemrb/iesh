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

# Compliant with IELister 40d421d0c87c570434ae5e46f4ea60703ac70671 and IESDP 2011-03-15 (more or less)

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
              'enum': { 1: 'no BAM', 2: 'single target', 3: 'area target' },
              'label': 'Projectile type' },

            { 'key': 'speed',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Speed' },


            { 'key': 'sparking_flag',
              'type': 'DWORD',
              'off': 0x000C,
              'mask': { 0x01: 'sparks', 0x02: 'use z coordinate', 0x04: 'loop sound', 0x08: 'loop sound2', 0x10: 'do not affect direct target', 0x20: 'draw below animate objects' },
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

            { 'key': 'x_gemrb_flags',
              'type': 'DWORD',
              'off': 0x002C,
              'label': '*GemRB flags'},

            { 'key': 'x_string_reference',
              'type': 'DWORD',
              'off': 0x0030,
              'label': '*String reference'},

            { 'key': 'x_color',
              'type': 'DWORD',
              'off': 0x0034,
              'label': '*Color'},

            { 'key': 'x_color_speed',
              'type': 'WORD',
              'off': 0x0038,
              'label': '*Color speed'},

            { 'key': 'x_shake',
              'type': 'WORD',
              'off': 0x003A,
              'label': '*Shake'},

            { 'key': 'x_ids_value',
              'type': 'WORD',
              'off': 0x003C,
              'label': '*IDS value'},

            { 'key': 'x_ids_type',
              'type': 'WORD',
              'off': 0x003E,
              'label': '*IDS type'},

            { 'key': 'x_ids_value_2',
              'type': 'WORD',
              'off': 0x0040,
              'label': '*IDS value 2'},

            { 'key': 'x_ids_type_2',
              'type': 'WORD',
              'off': 0x0042,
              'label': '*IDS type 2'},

            { 'key': 'x_fail_spell',
              'type': 'RESREF',
              'off': 0x0044,
              'label': '*Fail spell resref'},

            { 'key': 'x_success_spell',
              'type': 'RESREF',
              'off': 0x004C,
              'label': '*Success spell resref'},

            { 'key': 'unknown54',
              'type': 'BYTES',
              'off': 0x0054,
              'size': 172,
              'label': 'Unknown 54'},

            { 'key': 'travel_flags',
              'type': 'DWORD',
              'off': 0x0100,
              'mask': { 0x01: 'enable BAM coloring', 0x02: 'enable smoke', 0x04: 'unused', 0x08: 'enable area lighting usage', 0x10: 'enable area height usage', 0x20: 'enable shadow', 0x40: 'enable light spot', 0x80: 'enable brighten flags', 0x100: 'low level brighten', 0x200: 'high level brighten' },
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

            { 'key': 'light_spot_x_size',
              'type': 'WORD',
              'off': 0x0118,
              'label': 'Light spot X-size'},

            { 'key': 'light_spot_y_size',
              'type': 'WORD',
              'off': 0x011A,
              'label': 'Light spot Y-size'},

            { 'key': 'palette',
              'type': 'RESREF',
              'off': 0x011C,
              'label': 'Palette BMP'},

            { 'key': 'projectile_color',
              'type': 'BYTE',
              'off': 0x0124,
              'count': 7,
              'label': 'Projectile color'},

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
              'enum': { 1: 'dont face', 5: 'mirrored eastern direction (reduced granularity)', 9: 'reduced eastern direction (full granularity)', 16: 'not mirrored, not reduced' },
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
              'size': 172, # FIXME: IESDP has 176 here ..., ielister 172
              'label': 'Unknown 154'},

            )

    area_header_desc = (
            { 'key': 'aoe_flags',
              'type': 'DWORD',
              'off': 0x0200,
              'mask': {0x0001: 'stay visible at destination',
                       0x0002: 'triggered by inanimate objects',
                       0x0004: 'triggered on condition',
                       0x0008: 'trigger during delay',
                       0x0010: 'use secondary projectile',
                       0x0020: 'draw fragments',
                       0x0040: 'no self',
                       0x0080: 'no enemies',
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

            { 'key': 'x_spread_animation',
              'type': 'RESREF',
              'off': 0x0228,
              'label': '*Spread animation'},

            { 'key': 'x_secondary_animation',
              'type': 'RESREF',
              'off': 0x0230,
              'label': '*Secondary animation'},

            { 'key': 'x_area_sound',
              'type': 'RESREF',
              'off': 0x0238,
              'label': '*Area sound'},

            { 'key': 'x_gemrb_aoe_flags',
              'type': 'DWORD',
              'off': 0x0240,
              'label': '*GemRB AOE flags'},

            { 'key': 'x_dice_count',
              'type': 'WORD',
              'off': 0x0244,
              'label': '*Dice count'},

            { 'key': 'x_dice_sides',
              'type': 'WORD',
              'off': 0x0246,
              'label': '*Dice sides'},

            { 'key': 'unknown248',
              'type': 'BYTES',
              'off': 0x0248,
              'size': 176,
              'label': 'Unknown 248'},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'PRO'


    def read (self, stream):
        self.read_header (stream)
        if self.header['projectile_type'] == 3:
            self.read_area_header (stream)


    def printme (self):
        self.print_header ()
        if self.header['projectile_type'] == 3:
            self.print_area_header ()
        

    def read_area_header (self, stream):
        self.area_header = {}
        self.read_struc (stream, 0x0000, self.area_header_desc, self.area_header)
        
    def print_area_header (self):
        self.print_struc (self.area_header, self.area_header_desc)

        
register_format ('PRO', 'V1.0', PRO_Format)
