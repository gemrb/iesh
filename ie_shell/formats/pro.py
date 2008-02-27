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

# RCS: $Id: pro.py,v 1.1 2006/07/08 14:29:26 edheldil Exp $

from ie_shell.formats.format import Format, register_format, core

class PRO_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'PRO'


        self.header_desc = (
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
              'enum': { 2: 'single target', 3: 'area target' },
              'label': 'Projectile type' },

            { 'key': 'speed',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Speed' },


            { 'key': 'sparking_flag',
              'type': 'WORD',
              'off': 0x000C,
              'mask': { 0x01: 'sparks', 0x02: 'flying projectile', 0x04: 'looping sound', 0x08: 'unknown', 0x10: 'ignore centre' },
              'label': 'Sparking flag'},

            { 'key': 'unknown',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Unknown'},

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
              'label': 'Spark color'},



            { 'key': 'unknown2C',
              'type': 'BYTES',
              'off': 0x002C,
              'size': 212,
              'label': 'Unknown 2C'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0100,
              'mask': { 0x01: 'enable BAM coloring', 0x02: 'enable smoke', 0x04: 'unknown', 0x08: 'darken projectile', 0x10: 'unknown2', 0x20: 'enable shadow', 0x40: 'enable light spot', 0x80: 'colored shadow' },
              'label': 'Flags'},

            { 'key': 'projectile_bam',
              'type': 'RESREF',
              'off': 0x0104,
              'label': 'BAM for travelling projectile'},

            { 'key': 'shadow_bam',
              'type': 'RESREF',
              'off': 0x010C,
              'label': 'BAM for projectile shadow'},

            { 'key': 'projectile_bam_cycle',
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
              'type': 'BYTE',
              'off': 0x0118,
              'label': 'Light spot X-size'},

            { 'key': 'invisible',
              'type': 'BYTE',
              'off': 0x0119,
              'label': 'Invisible'},

            { 'key': 'light_spot_y_size',
              'type': 'WORD',
              'off': 0x011A,
              'label': 'Light spot Y-size'},

            { 'key': 'travel_type_color_bmp',
              'type': 'RESREF',
              'off': 0x011C,
              'label': 'Travel-type projectile color BMP'},

            { 'key': 'projectile_color',
              'type': 'BYTE',
              'off': 0x0124,
              'label': 'Projectile color'},

            { 'key': 'projectile_color_gradients',
              'type': 'BYTES',
              'off': 0x0125,
              'size': 6,
              'label': 'Projectile color gradients'},

            { 'key': 'smoke_puff_timing',
              'type': 'BYTE',
              'off': 0x012B,
              'label': 'Smoke puff timing'},

            { 'key': 'smoke_color',
              'type': 'BYTE',
              'off': 0x012C,
              'label': 'Smoke color'},

            { 'key': 'smoke_color_gradients',
              'type': 'BYTES',
              'off': 0x012D,
              'size': 6,
              'label': 'Smoke color gradients'},

            { 'key': 'face_target',
              'type': 'BYTE',
              'off': 0x0133,
              'enum': { 1: 'dont face', 5: 'face' },
              'label': 'Face target'},

            { 'key': 'smoke_reference',
              'type': 'WORD', # FIXME: should be signed??
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
              'size': 176,
              'label': 'Unknown 154'},

            )

        self.area_header_desc = (
            { 'key': 'aoe_target',
              'type': 'WORD',
              'off': 0x0200,
              'mask': {0x0001: 'trap object visible',
                       0x0002: 'triggered by inanimate objects',
                       0x0004: 'triggered on condition',
                       0x0008: 'single explosion',
                       0x0010: 'no allies',
                       0x0020: 'draw fragments',
                       0x0040: 'no self',
                       0x0080: 'no enemies',
                       0x0100: 'unknown 8',
                       0x0200: 'multiple set off',
                       0x0400: 'use VVC',
                       0x0800: 'cone shape',
                       0x1000: 'unknown 12',
                       0x2000: 'no explosion?',
                       0x4000: 'delayed explosion?',
                       0x8000: 'affect only one' },
              'label': 'AOE target (enemies/allies)'},

            { 'key': 'unknown202',
              'type': 'WORD',
              'off': 0x0202,
              'label': 'Unknown 202'},

            { 'key': 'trigger_radius',
              'type': 'WORD',
              'off': 0x0204,
              'label': 'Trigger radius'},

            { 'key': 'area_of_effect',
              'type': 'WORD',
              'off': 0x0206,
              'label': 'Area of Effect'},

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

            { 'key': 'unknown214',
              'type': 'WORD',
              'off': 0x0214,
              'label': 'Unknown 214'},

            { 'key': 'duration_count',
              'type': 'BYTE',
              'off': 0x0216,
              'label': 'Duration/Trigger count'},

            { 'key': '1st_explosion_projectile',
              'type': 'BYTE',
              'off': 0x0217,
              'enum': 'FIREBALL',
              'label': '1st explosion projectile ref to FIREBALL.IDS'},

            { 'key': '1st_explosion_color',
              'type': 'BYTE',
              'off': 0x0218,
              'label': '1st explosion color'},

            { 'key': 'unknown219',
              'type': 'BYTE',
              'off': 0x0219,
              'label': 'Unknown 219'},

            { 'key': 'explosion_projectile',
              'type': 'WORD',
              'off': 0x021A,
              'enum': 'PROJECTL',
              'label': 'Explosion projectile ref to PROJECTL.IDS'},

            { 'key': 'vvc',
              'type': 'RESREF',
              'off': 0x021C,
              'label': 'VVC'},

            { 'key': 'cone_width',
              'type': 'WORD',
              'off': 0x0224,
              'label': 'Cone width'},

            { 'key': 'unknown226',
              'type': 'BYTES',
              'off': 0x0226,
              'size': 218,
              'label': 'Unknown 218'},

            )



    def decode_file (self):
        self.decode_header ()
        if self.header['projectile_type'] == 3:
            self.decode_area_header ()


    def print_file (self):
        self.print_header ()
        if self.header['projectile_type'] == 3:
            self.print_area_header ()


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_area_header (self):
        self.area_header = {}
        self.decode_by_desc (0x0000, self.area_header_desc, self.area_header)
        
    def print_area_header (self):
        self.print_by_desc (self.area_header, self.area_header_desc)

        
register_format ('PRO', 'V1.0', PRO_Format)
