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


from infinity import core
from infinity.format import Format, register_format

class VVC_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'animation',
              'type': 'RESREF',
              'off': 0x0008,
              'label': 'Animation BAM' },

            { 'key': 'unknown_10',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Unknown 10' },

            { 'key': 'unknown_14',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Unknown 14' },

            { 'key': 'misc_flags',
              'type': 'WORD',
              'off': 0x0018,
              'mask': {
                  0x0001: 'unknown 0',
                  0x0002: 'translucent',
                  0x0004: 'unknown 2',
                  0x0008: 'transparent',
                  0x0010: 'mirror Y axis',
                  0x0020: 'mirror X axis',
                  0x0040: 'unknown 6',
                  0x0080: 'unknown 7',
                  0x0100: 'unknown 8',
                  0x0200: 'blend',
                  0x0400: 'unknown 10',
                  0x0800: 'unknown 11',
                  0x1000: 'unknown 12',
                  0x2000: 'unknown 13',
                  0x4000: 'unknown 14',
                  0x8000: 'unknown 15',
                  },
              'label': 'Misc. flags'},

            { 'key': 'tint',
              'type': 'WORD',
              'off': 0x001A,
              'mask': {
                  0x0001: 'unknown 0',
                  0x0002: 'unknown 1',
                  0x0004: 'unknown 2',
                  0x0008: 'greyscale',
                  0x0010: 'unknown 4',
                  0x0020: 'glowing',
                  0x0040: 'unknown 6',
                  0x0080: 'unknown 7',
                  0x0100: 'unknown 8',
                  0x0200: 'red',
                  0x0400: 'unknown 10',
                  0x0800: 'unknown 11',
                  0x1000: 'unknown 12',
                  0x2000: 'unknown 13',
                  0x4000: 'unknown 14',
                  0x8000: 'unknown 15',
                  },
              'label': 'Tint'},

            { 'key': 'unknown_1C',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Unknown 1C'},

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0020,
              'mask': {
                  0x0001: 'looping',
                  0x0002: 'sequence 2',
                  0x0004: 'sequence 4',
                  0x0008: 'greyscale',
                  0x0010: 'unknown 4',
                  0x0020: 'unknown 5',
                  0x0040: 'wallgrps do not cover',
                  0x0080: 'unknown 7',
                  0x0100: 'use bam',
                  0x0200: 'unknown 9',
                  0x0400: 'unknown 10',
                  0x0800: 'unknown 11',
                  0x1000: 'unknown 12',
                  0x2000: 'unknown 13',
                  0x4000: 'unknown 14',
                  0x8000: 'unknown 15',
                  },
              'label': 'Flags'},

            { 'key': 'unknown_24',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Unknown 24'},

            { 'key': 'x_pos',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'X position'},

            { 'key': 'y_pos',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Y position'},

            { 'key': 'unknown_30',
              'type': 'DWORD',
              'off': 0x0030,
              'label': 'Unknown 30'},

            { 'key': 'frame_rate',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Frame rate'},

            { 'key': 'face_target', # FIXME: ielister has unknown here
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'Face target'},

            { 'key': 'unknown_3C',
              'type': 'DWORD',
              'off': 0x003C,
              'label': 'Unknown 3C'},

            { 'key': 'position',
              'type': 'DWORD',
              'off': 0x0040,
              'mask': { 0x1: 'orbit target', 0x2: 'rel. to target' },
              'label': 'Position'},

            { 'key': 'unknown_44',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Unknown 44'},

            { 'key': 'unknown_48',
              'type': 'DWORD',
              'off': 0x0048,
              'label': 'Unknown 48'},

            { 'key': 'z_pos',
              'type': 'DWORD',
              'off': 0x004C,
              'label': 'Z position'},

            { 'key': 'unknown_50',
              'type': 'DWORD',
              'off': 0x0050,
              'label': 'Unknown 50'},

            { 'key': 'unknown_54',
              'type': 'RESREF',
              'off': 0x0054,
              'label': 'Unknown 54'},

            { 'key': 'duration',
              'type': 'DWORD',
              'off': 0x005C,
              'label': 'Duration'},

            { 'key': 'unknown_60',
              'type': 'RESREF',
              'off': 0x0060,
              'label': 'Unknown 60'},

            { 'key': 'introduction_bam_cycle',
              'type': 'DWORD',
              'off': 0x0068,
              'label': 'Introduction BAM cycle'},

            { 'key': 'duration_bam_cycle',
              'type': 'DWORD',
              'off': 0x006C,
              'label': 'Duration BAM cycle'},

            { 'key': 'unknown_70',
              'type': 'RESREF',
              'off': 0x0070,
              'label': 'Unknown 70'},

            { 'key': 'introduction_wavc',
              'type': 'RESREF',
              'off': 0x0078,
              'label': 'Introduction WAVC'},

            { 'key': 'duration_wavc',
              'type': 'RESREF',
              'off': 0x0080,
              'label': 'Duration WAVC'},

            { 'key': 'unknown_88',
              'type': 'DWORD',
              'off': 0x0088,
              'label': 'Unknown 88'},

            { 'key': 'unknown_8C',
              'type': 'DWORD',
              'off': 0x008C,
              'label': 'Unknown 8C'},

            { 'key': 'ending_bam_cycle', # FIXME: ielister has unknown here
              'type': 'DWORD',
              'off': 0x0090,
              'label': 'Ending BAM cycle'},

            { 'key': 'ending_wavc', # FIXME: ielister has unknown here
              'type': 'RESREF',
              'off': 0x0094,
              'label': 'Ending WAVC?'},

            { 'key': 'unknown_9C',
              'type': 'BYTES',
              'off': 0x009C,
              'size': 336,
              'label': 'Unknown 9C'},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'VVC'

    def read (self, stream):
        self.read_header (stream)

    def write (self, stream):
        self.write_header (stream)

    def printme (self):
        self.print_header ()


        
register_format (VVC_Format, signature='VVC V1.0', extension='VVC', name='VVC', type=0x3fb)
