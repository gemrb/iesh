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

# XXConforming to IESDP 4.2.2009

import struct
import sys

from infinity.format import Format, register_format
from infinity.image import Image


class PLT_Format (Format, Image):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'unknown_08',
                'type': 'WORD',
                'off': 0x0008,
                'label': 'Unknown 08' },

            { 'key': 'unknown_0A',
                'type': 'WORD',
                'off': 0x000A,
                'label': 'Unknown 0A' },

            { 'key': 'unknown_0C',
                'type': 'WORD',
                'off': 0x000C,
                'label': 'Unknown 0C' },

            { 'key': 'unknown_0E',
                'type': 'WORD',
                'off': 0x000E,
                'label': 'Unknown 0E' },

            { 'key': 'width',
                'type': 'DWORD',
                'off': 0x0010,
                'label': 'Width' },

            { 'key': 'height',
                'type': 'DWORD',
                'off': 0x0014,
                'label': 'Height' },

            )


    def __init__ (self):
        Format.__init__ (self)
        Image.__init__ (self)
        self.expect_signature = 'PLT'
        self.palettes = None


    def read (self, stream):
        self.read_header (stream)
        size = self.header['width'] * self.header['height']
        self.raw_pixels = stream.read_blob (0x0018, size * 2)
        self.decode()


    def decode (self):
        size = self.header['width'] * self.header['height']
        data = [ '\0\0\0\0' ] * size
        pixels = self.raw_pixels
        
        for i in range (size):
            intensity = ord (pixels[2*i])
            palindex = ord (pixels[2*i+1])
            a = (255, 0)[intensity == 255]
            # FIXME: shadows have full alpha
            
            if self.palettes:
                (r, g, b) = self.palettes[palindex][intensity]
                pix = '%c%c%c%c' %(r, g, b, a)
            else:
                pix = '%c%c%c%c' %(intensity, intensity, intensity, a)

            x = i % self.header['width']
            y = self.header['height'] - i / self.header['width'] -1
            data[y * self.header['width'] + x] = pix
            
        self.pixels = ''.join (data)
        

    def write (self, stream):
        self.write_header (stream)
        size = self.header['width'] * self.header['height']
        stream.write_blob (self.raw_pixels, 0x0018, size * 2)


    def printme (self):
        self.print_header ()
        
        if self.get_option ('format.plt.print_bitmap'):
            self.print_bitmap ()
            print


register_format ('PLT', 'V1', PLT_Format)
