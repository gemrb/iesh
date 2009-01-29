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


import struct
import sys

from infinity.format import Format, register_format
from infinity.stream import CompressedStream


class MOS_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'Width (pixels)'},
            
            { 'key': 'height',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Height (pixels)'},

            { 'key': 'columns',
              'type': 'WORD',
              'off': 0x000C,
              'label': 'Columns (blocks)'},

            { 'key': 'rows',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Rows (blocks)'},

            { 'key': 'block_size',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Block size (pixels)'},

            { 'key': 'palette_off',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Palettes offset'},
            )

    # NOTE: not actually used
    tile_desc = (
            { 'key': 'tile_data',
              'type': '_BYTES',
              'off': 0x0000,
              'label': 'Tile data'},

            { 'key': 'palette',
              'type': '_BYTES',
              'off': 0x0000,
              'label': 'Palette'},
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
        self.expect_signature = 'MOS'

        self.tile_list = []


    def read (self, stream):
        self.read_header (stream)

        tile_cnt = self.header['columns'] * self.header['rows']
        off = self.header['palette_off']
        offset_tiles = self.header['palette_off'] + tile_cnt * (256 * 4 + 4)
        
        for i in range (tile_cnt):
            obj = {}
            palette = []
            self.read_palette (stream, off, palette)
            obj['palette'] = palette
            self.tile_list.append (obj)
            off += 256 * 4

        i = 0
        for y in range (self.header['rows']):
            for x in range (self.header['columns']):
                obj = self.tile_list[i]
                obj['width'] = min (self.header['width'] - x * self.header['block_size'], self.header['block_size'])
                obj['height'] = min (self.header['height'] - y * self.header['block_size'], self.header['block_size'])
                obj['offset'] = offset_tiles + stream.read_dword (off)
                
                self.read_tile (stream, obj)
                off += 4
                i += 1

        return self


    def printme (self):
        self.print_header ()

        if self.get_option ('format.mos.print_palettes'):
            i = 0
            for obj in self.tile_list:
                print 'Palette #%d' %i
                self.print_palette (obj['palette'])
                i = i + 1

        if self.get_option ('format.mos.print_tiles'):
            i = 0
            for obj in self.tile_list:
                print 'Tile #%d' %i
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

    def print_palette (self, palette):
        i = 0
        for obj in palette:
            print "%3d: %3d %3d %3d %3d (#%02x%02x%02x%02x)" %(i, obj['r'], obj['g'], obj['b'], obj['a'], obj['r'], obj['g'], obj['b'], obj['a'])
            i = i + 1


    def read_tile (self, stream, obj):
        size = obj['width'] * obj['height']
        bin_data = stream.read_blob (obj['offset'], size)
        obj['tile_data'] = struct.unpack ('%dB' %size, bin_data)


    def print_tile (self, obj):
        gray = ' #*+:.'
        grsz = len (gray) - 1
        ndx = 0

        for i in range (obj['height']):
            for j in range (obj['width']):
                pix = obj['tile_data'][ndx]

                p = obj['palette'][pix]
                gr = 1 + (p['r'] + p['g'] + p['b']) / (3 * (255 / grsz))
                if gr >= grsz:
                    gr = grsz - 1
                sys.stdout.write (gray[gr])
                #sys.stdout.write (gray[gr])
                #print gray[gr],
                ndx = ndx + 1
            print
        print
    
    # FIXME: use stream instead of fh?
    def write_ppm (self, fh):
        fh.write ("P6\n")
        fh.write ("# ie_shell\n");
        fh.write ("%d %d\n" %(self.header['width'], self.header['height']));
        fh.write ("255\n");

        for line in range (self.header['height']):
            row = line / self.header['block_size']
            scanline = line % self.header['block_size']
            
            for i in range (self.header['columns']):
                tile = self.tile_list[(row * self.header['columns']) + i]
                pal = tile['palette']
            
                o = scanline * tile['width']
                for x in range (tile['width']):
                    pix = tile['tile_data'][o + x]
                    col = pal[pix]
                    fh.write ('%c%c%c' %(col['r'], col['g'], col['b']))


class MOSC_Format (MOS_Format):
    envelope_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'uncompressed_size',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Uncompressed size'},
            
            )

    def __init__ (self):
        MOS_Format.__init__ (self)
        self.expect_signature = 'MOSC'


    def read (self, stream):
        self.read_envelope (stream)
        # FIXME: size??
        data = stream.read_blob (0x0C)

        #self.stream.close ()
        stream = CompressedStream ().open (data)

        return MOS_Format.read (self, stream)

    def printme (self):
        self.print_envelope ()
        MOS_Format.printme (self)

    def read_envelope (self, stream):
        self.envelope = {}
        self.read_struc (stream, 0x0000, self.envelope_desc, self.envelope)
        
    def print_envelope (self):
        self.print_struc (self.envelope, self.envelope_desc)
        



register_format ('MOS', 'V1', MOS_Format)
register_format ('MOSC', 'V1', MOSC_Format)
