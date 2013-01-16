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

import struct
import sys
import PIL

from infinity import core
from infinity.format import Format, register_format
from infinity.imagesequence import ImageSequence

class TIS_Format (Format, ImageSequence):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'tile_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Count of tiles' },

            { 'key': 'length',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Tile size (bytes)' },


            { 'key': 'tile_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Tiles offset'},

            { 'key': 'size',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Tile width (or height)'},

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
        ImageSequence.__init__ (self)
        self.expect_signature = 'TIS'

        self.tile_list = []


    def read (self, stream):
        self.read_header (stream)

        palette_size = 4 * 256
        tile_size = self.header['size'] ** 2
        
        off = self.header['tile_off']
        for i in range (self.header['tile_cnt']):
            pal = []
            self.read_palette (stream,  off,  pal)
            off += palette_size
            bin_data = stream.read_blob (off, tile_size)
            #tile_data = struct.unpack ('%dB' %tile_size, bin_data)
            off += tile_size
            obj = {'palette': pal,  'tile_data': bin_data}
            
            self.tile_list.append (obj)

        return self


    def write (self,  stream):
        self.header['tile_cnt'] = len (self.tile_list)
        self.header['tile_off'] = self.get_struc_size (self.header_desc)
        self.write_header (stream)

        tile_size = self.header['size'] ** 2
        palette_size = 4 * 256
        
        off = self.header['tile_off'] 
        
        for tile in self.tile_list:
            self.write_palette (stream, off, tile['palette'])
            off += palette_size
            #bin_data = struct.pack ('%dB' %tile_size, *tile['tile_data'])
            stream.write_blob (tile['tile_data'], off)
            
            off += tile_size


    def printme (self):
        self.print_header ()

        if self.get_option ('format.tis.print_palettes'):
            i = 0
            for obj in self.tile_list:
                print('Palette #%d' %i)
                self.print_palette (obj['palette'])
                i = i + 1

        if self.get_option ('format.tis.print_tiles'):
            i = 0
            for obj in self.tile_list:
                print('Tile #%d' %i)
                #print obj['offset']
                self.print_tile (obj)
                i = i + 1


    def read_palette (self, stream, offset, obj):
        for i in range (256):
            obj2 = {}
            self.read_struc (stream, offset, self.palette_entry_desc, obj2)
            obj.append (obj2)
            offset = offset + 4

        return obj

    def write_palette (self, stream, offset, obj):
        for i in range (256):
            self.write_struc (stream, offset, self.palette_entry_desc, obj[i])
            offset = offset + 4


    def print_palette (self, palette):
        i = 0
        for obj in palette:
            print("%3d: %3d %3d %3d %3d (#%02x%02x%02x%02x)" %(i, obj['r'], obj['g'], obj['b'], obj['a'], obj['r'], obj['g'], obj['b'], obj['a']))
            i = i + 1


#    def read_tile (self, stream, obj):
#        size = obj['width'] * obj['height']
#        bin_data = stream.read_blob (obj['offset'], size)
#        obj['tile_data'] = struct.unpack ('%dB' %size, bin_data)
#
# 
    def frame_to_image (self, obj):
        pal = obj['palette']
        data = [ '%c%c%c\xff' %(pal[ord(p)]['r'], pal[ord(p)]['g'], pal[ord(p)]['b'])  for p in obj['tile_data']]
        pixels = ''.join(data)
        # FIXME: not needed 
        obj['x'] = 0
        obj['y'] = 0
        sz = self.header['size']
        obj['width'] = sz
        obj['height'] = sz

        img = PIL.Image.fromstring ('RGBA', (sz, sz), pixels, "raw", 'RGBA', 0, 1)
        img.x = 0
        img.y = 0

        obj['image'] = img
        return img

#    def print_tile (self, obj):
#        gray = ' #*+:.'
#        grsz = len (gray) - 1
#        ndx = 0
#
#        for i in range (self.header['size']):
#            for j in range (self.header['size']):
#                pix = obj['tile_data'][ndx]
#
#                p = obj['palette'][pix]
#                gr = 1 + (p['r'] + p['g'] + p['b']) / (3 * (255 / grsz))
#                if gr >= grsz:
#                    gr = grsz - 1
#                sys.stdout.write (gray[gr])
#                #sys.stdout.write (gray[gr])
#                #print gray[gr],
#                ndx = ndx + 1
#            print
#        print

#    # FIXME: use stream instead of fh?
#    def write_ppm (self, fh):
#        fh.write ("P6\n")
#        fh.write ("# ie_shell\n");
#        fh.write ("%d %d\n" %(self.header['width'], self.header['height']));
#        fh.write ("255\n");
#
#        for line in range (self.header['height']):
#            row = line / self.header['block_size']
#            scanline = line % self.header['block_size']
#            
#            for i in range (self.header['columns']):
#                tile = self.tile_list[(row * self.header['columns']) + i]
#                pal = tile['palette']
#            
#                o = scanline * tile['width']
#                for x in range (tile['width']):
#                    pix = tile['tile_data'][o + x]
#                    col = pal[pix]
#                    fh.write ('%c%c%c' %(col['r'], col['g'], col['b']))


    def get_frame_lol (self):
        return [ self.tile_list ]

    def from_mos (self, mos):
        self.tile_list = []
        size = self.header['size'] = mos.header['block_size']
        
        for obj in mos.tile_list:
            # FIXME: this destroys original tiles in the MOS_Format object
            width = obj['width']
            height = obj['height']
            
            if width < size:
                pad = [ obj['tile_data'][size - 1] ] * (size - width)
            else:
                pad = []
            
            #print 'Pad:', pad
            start = 0
            data = []
            for i in range (obj['height']):
                row = list (obj['tile_data'][start:start+width]) + pad
                data.extend (row)
                
                start += width


            if height < size:
                pad = data[-size:] * (size - height)
            else:
                pad = []
            
            #print 'Pad:', pad
            data.extend (pad)
            data = struct.pack ("%dB" %(size*size), *data)
            self.tile_list.append ({ 'palette': obj['palette'], 'tile_data': data })

        self.header['tile_cnt'] = len (self.tile_list)
        self.header['tile_off'] = self.get_struc_size (self.header_desc)
        self.header['length'] = 4 * 256 + self.header['size'] ** 2


class UTIS_Format (TIS_Format):
    def __init__ (self):
        TIS_Format.__init__ (self)
        
        self.header = {}
        self.reset_struc (self.header_desc, self.header)
        self.header['size'] = 64


    def read (self, stream):
        #self.read_header (stream)

        palette_size = 4 * 256
        tile_size = self.header['size'] ** 2
        
        off = 0
        while True:
            pal = []
            try:
                self.read_palette (stream,  off,  pal)
            except: # FIXME: ugly hack
                break
            
            off += palette_size
            bin_data = stream.read_blob (off, tile_size)
            if len (bin_data) != tile_size:
                break
            off += tile_size
            obj = {'palette': pal,  'tile_data': bin_data}
            
            self.tile_list.append (obj)

        self.header['tile_cnt'] = len (self.tile_list)
        return self


register_format ('TIS', 'V1', TIS_Format)
