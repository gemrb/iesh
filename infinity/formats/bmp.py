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

# Conforms to GemRB e31133f8 (2012-08-23), BMPImporter

import sys

from infinity.format import Format, register_format
from infinity.image import Image


class BMP_Format (Format, Image):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR2',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'size',
              'type': 'DWORD',
              'off':0x0002,
              'label': 'File size'},
            
            { 'key': 'reserved',
              'type': 'DWORD',
              'off': 0x0006,
              'label': 'Reserved(=0)'},
            
            { 'key': 'data_off',
              'type': 'DWORD',
              'off': 0x000A,
              'label': 'Data offset'},


            { 'key': 'info_size',
              'type': 'DWORD',
              'off': 0x000E,
              'label': 'Info header size'},

            { 'key': 'width',
              'type': 'DWORD',
              'off': 0x0012,
              'label': 'Width'},

            { 'key': 'height',
              'type': 'DWORD',
              'off': 0x0016,
              'label': 'Height'},

            { 'key': 'planes',
              'type': 'WORD',
              'off': 0x001A,
              'label': 'Num of planes(=1)'},

            { 'key': 'bpp',
              'type': 'WORD',
              'off': 0x001C,
              'label': 'Bits per pixel'},

            { 'key': 'compression',
              'type': 'DWORD',
              'off': 0x001E,
              'label': 'Compression'},

            { 'key': 'data_size',
              'type': 'DWORD',
              'off': 0x0022,
              'label': 'Raster data size'},

            { 'key': 'x_resolution',
              'type': 'DWORD',
              'off': 0x0026,
              'label': 'Horizontal Resolution [pixels/meter]'},

            { 'key': 'y_resolution',
              'type': 'DWORD',
              'off': 0x002A,
              'label': 'Vertical Resolution [pixels/meter]'},

            { 'key': 'colors',
              'type': 'DWORD',
              'off': 0x002E,
              'label': 'Number of colors used'},

            { 'key': 'important_colors',
              'type': 'DWORD',
              'off': 0x0032,
              'label': 'Number of important colors(0=all)'},
            )

    palette_entry_desc = (
            { 'key': 'b',
              'type': 'BYTE',
              'off': 0x0000,
              'label': 'B'},

            { 'key': 'g',
              'type': 'BYTE',
              'off': 0x0001,
              'label': 'G'},

            { 'key': 'r',
              'type': 'BYTE',
              'off': 0x0002,
              'label': 'R'},

            { 'key': 'a',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'A'},
            )


    def __init__ (self):
        Format.__init__ (self)
        Image.__init__ (self)
        self.expect_signature = 'BM'

        self.palette_entry_list = []


    def read (self, stream):
        self.read_header (stream)

        if self.header['info_size'] < 24:
            raise ValueError ("OS/2 bitmaps not supported")

        if self.header['compression']:
            raise ValueError ("Compressed bitmaps not supported")

        width = self.header['width']
        height = self.header['height']
        bpp = self.header['bpp']

        if bpp <= 8:
            off = self.get_struc_size (self.header_desc)
            self.read_palette (stream, off)

        if bpp == 32:
            padded_len = width * 4
        elif bpp == 24:
            padded_len = width * 3
        elif bpp == 16:
            padded_len = width * 2
        elif bpp == 8:
            padded_len = width
        elif bpp == 4:
            padded_len = width >> 1
        else:
            raise ValueError ("Bpp %d not supported" %bpp)
        
        if padded_len & 3:
            padded_len += (4 - (padded_len & 3))

        size = padded_len * height
        self.pixels_raw = stream.read_blob (self.header['data_off'], size)

        data = [ '\0\0\0\0' ] * (width * height)
        
        if bpp == 32:
            self.decode_32bit_uncompressed (width, height, padded_len, data)
        elif bpp == 24:
            self.decode_24bit_uncompressed (width, height, padded_len, data)
        #elif bpp == 16:
        #    self.decode_16bit_uncompressed (width, height, padded_len, data)
        elif bpp == 8:
            self.decode_8bit_uncompressed (width, height, padded_len, data)
        elif bpp == 4:
            self.decode_4bit_uncompressed (width, height, padded_len, data)

        self.pixels = ''.join (data)


    def decode_4bit_uncompressed (self, width, height, padded_len, data):
        src = 0

        for y in range (height):
            for x in range (width):
                if x & 1:
                    nib = ord (self.pixels_raw[src+x/2]) & 15
                else:
                    nib = (ord (self.pixels_raw[src+x/2]) >> 4) & 15
                    
                c = self.palette_entry_list[nib]
                pix = '%c%c%c\xff' %(c['r'], c['g'], c['b'])
                data[(height-y-1) * width + x] = pix
            src += padded_len


    def decode_8bit_uncompressed (self, width, height, padded_len, data):
        src = 0

        for y in range (height):
            for x in range (width):
                c = self.palette_entry_list[ord (self.pixels_raw[src+x])]
                pix = '%c%c%c\xff' %(c['r'], c['g'], c['b'])
                data[(height-y-1) * width + x] = pix
            src += padded_len


    def decode_24bit_uncompressed (self, width, height, padded_len, data):
        src = 0
        p = self.pixels_raw
        
        for y in range (height):
            for x in range (width):
                pix = '%c%c%c\xff' %(p[src+3*x+2], p[src+3*x+1], p[src+3*x])
                data[(height-y-1) * width + x] = pix
            src += padded_len


    def decode_32bit_uncompressed (self, width, height, padded_len, data):
        src = 0
        p = self.pixels_raw
        
        for y in range (height):
            for x in range (width):
                pix = '%c%c%c%c' %(p[src+4*x+2], p[src+4*x+1], p[src+4*x], p[src+4*x+3])
                data[(height-y-1) * width + x] = pix
            src += padded_len


    def printme (self):
        self.print_header ()
        self.print_palette()

        if self.get_option ('format.bmp.print_palette'):
            self.print_palette ()

        if self.get_option ('format.bmp.print_bitmap'):
            self.print_bitmap ()
            print


    def read_palette (self, stream, offset):
        if self.header['colors']:
            numcolors = self.header['colors']
        elif self.header['bpp'] == 8:
            numcolors = 256
        else:
            numcolors = 16
                    
        for i in range (numcolors):
            obj = {}
            self.read_struc (stream, offset, self.palette_entry_desc, obj)
            self.palette_entry_list.append (obj)

            offset = offset + 4


    def print_palette (self):
        for i, obj in enumerate (self.palette_entry_list):
            print "%3d: %3d %3d %3d %3d (#%02x%02x%02x%02x)" %(i, obj['r'], obj['g'], obj['b'], obj['a'], obj['r'], obj['g'], obj['b'], obj['a'])
        


register_format ('BM', '', BMP_Format)
