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

# RCS: $Id: bam.py,v 1.3 2006/07/08 14:29:26 edheldil Exp $

import struct
import sys

from ie_shell.formats.format import Format, register_format
from ie_shell.formats.stream import CompressedStream


class BAM_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'BAM'

        self.frame_list = []
        self.cycle_list = []
        self.palette_entry_list = []
        self.frame_lut_entry_list = []


        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'frame_cnt',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'Frame count'},
            
            { 'key': 'cycle_cnt',
              'type': 'BYTE',
              'off': 0x000A,
              'label': 'Cycle count'},

            { 'key': 'comp_color_ndx',
              'type': 'BYTE',
              'off': 0x000B,
              'label': 'Compressed color index'},

            { 'key': 'transp_color_ndx',
              'type': '_BYTE',
              'off': 0x000B,
              'label': 'Transparent color index'},

            { 'key': 'frame_off',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Frame and Cycle entries offset'},

            { 'key': 'palette_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Palette offset'},

            { 'key': 'frame_lut_off',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Frame lookup table offset'},
            )


        self.frame_desc = (
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Frame width'},

            { 'key': 'height',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Frame height'},

            { 'key': 'xcenter',
              'type': 'WORD',
              'off': 0x0004,
              'label': 'Frame center X'},

            { 'key': 'ycenter',
              'type': 'WORD',
              'off': 0x0006,
              'label': 'Frame center Y'},

            { 'key': 'rle_encoded',
              'type': 'DWORD',
              'off': 0x0008,
              'bits': '31-31',
              'label': 'RLE encoded'},

            { 'key': 'frame_data_off',
              'type': 'DWORD',
              'off': 0x0008,
              'bits': '30-0',
              'label': 'Frame data offset'},
            )

        self.cycle_desc = (
            { 'key': 'frame_cnt',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Frame count'},

            { 'key': 'frame_lut_ndx',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Frame LUT index'},

            { 'key': 'frames',
              'type': '_STRING',
              'off': 0x0000,
              'label': 'Frame indices'},
            )

        self.palette_entry_desc = (
            { 'key': 'r',
              'type': 'BYTE',
              'off': 0x0000,
              'label': 'R'},

            { 'key': 'g',
              'type': 'BYTE',
              'off': 0x0001,
              'label': 'G'},

            { 'key': 'b',
              'type': 'BYTE',
              'off': 0x0002,
              'label': 'B'},

            { 'key': 'a',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'A'},
            )

        self.frame_lut_entry_desc = (
            { 'key': 'frame',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Frame'},
            )

    def decode_file (self):
        self.decode_header ()

        off = self.header['frame_off']
        for i in range (self.header['frame_cnt']):
            obj = {}
            self.decode_frame (off, obj)
            self.frame_list.append (obj)
            off = off + 12

        for i in range (self.header['cycle_cnt']):
            obj = {}
            self.decode_cycle (off, obj)
            self.cycle_list.append (obj)
            off = off + 4

        self.decode_palette (self.header['palette_off'])


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.frame_list:
            print 'Frame #%d' %i
            self.print_frame (obj)
            i = i + 1

        i = 0
        for obj in self.cycle_list:
            print 'Cycle #%d' %i
            self.print_cycle (obj)
            i = i + 1

        if self.get_option ('bam_print_palette'):
            self.print_palette ()


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_frame (self, offset, obj):
        self.decode_by_desc (offset, self.frame_desc, obj)

        if self.get_option ('bam_decode_frame_data'):
            if self.get_option ('bam_force_rle') or obj['rle_encoded']:
                self.decode_rle_frame_data (obj)
            else:
                self.decode_frame_data (obj)
    
    def print_frame (self, obj):
        self.print_by_desc (obj, self.frame_desc)

        if self.get_option ('bam_print_frame_bitmap'):
            self.print_frame_bitmap (obj)

    def decode_cycle (self, offset, obj):
        self.decode_by_desc (offset, self.cycle_desc, obj)
        obj['frame_list'] = []
        
        off2 = self.header['frame_lut_off'] + 2 * obj['frame_lut_ndx']
        obj2 = {}
        for i in range (obj['frame_cnt']):
            self.decode_by_desc (off2, self.frame_lut_entry_desc, obj2)
            obj['frame_list'].append (obj2['frame'])
            obj['frames'] = obj['frames'] + str(obj2['frame']) + ' '
            off2 = off2 + 2

    def print_cycle (self, obj):
        self.print_by_desc (obj, self.cycle_desc)


    def decode_palette (self, offset):
        transp_color = None
        
        for i in range (256):
            obj = {}
            self.decode_by_desc (offset, self.palette_entry_desc, obj)
            self.palette_entry_list.append (obj)

            if transp_color == None and obj['r'] == 0 and obj['g'] == 255 and obj['b'] == 0:
                transp_color = i

            offset = offset + 4

        if transp_color == None:
            transp_color = 0
        self.header['transp_color_ndx'] = transp_color


    def print_palette (self):
        i = 0
        for obj in self.palette_entry_list:
            print "%3d: %3d %3d %3d %3d (#%02x%02x%02x%02x)" %(i, obj['r'], obj['g'], obj['b'], obj['a'], obj['r'], obj['g'], obj['b'], obj['a'])
            i = i + 1


    def decode_frame_data (self, obj):
        size = obj['width'] * obj['height']
        bin_data = self.stream.decode_blob (obj['frame_data_off'], size)
        obj['frame_data'] = struct.unpack ('%dB' %size, bin_data)

    def decode_rle_frame_data (self, obj):
        off = obj['frame_data_off']
        size = obj['width'] * obj['height']
        compressed_color = self.header['comp_color_ndx']

        data = []
        while len (data) < size:
            pix = struct.unpack ('B', self.stream.get_char (off))[0]
            if pix == compressed_color:
                off = off + 1
                cnt = struct.unpack ('B', self.stream.get_char (off))[0]
                for j in range (cnt + 1):
                    data.append (compressed_color)
            else:
                data.append (pix)

            off = off + 1
            
        obj['frame_data'] = data

    def print_frame_data (self, obj):
        ndx = 0
        for i in range (obj['height']):
            for j in range (obj['width']):
                print '%3d' %obj['frame_data'][ndx],
                ndx = ndx + 1
            print
        print

    def print_frame_bitmap (self, obj):
        gray = ' #*+:.'
        grsz = len (gray) - 1
        transparent_color = self.header['transp_color_ndx']
        ndx = 0
        for i in range (obj['height']):
            for j in range (obj['width']):
                pix = obj['frame_data'][ndx]
                if pix == transparent_color:
                    gr = 0
                else:
                    p = self.palette_entry_list[pix]
                    gr = 1 + (p['r'] + p['g'] + p['b']) / (3 * (255 / grsz))
                    if gr >= grsz:
                        gr = grsz - 1
                sys.stdout.write (gray[gr])
                #sys.stdout.write (gray[gr])
                #print gray[gr],
                ndx = ndx + 1
            print
        print
        


class BAMC_Format (BAM_Format):
    def __init__ (self, filename):
        BAM_Format.__init__ (self, filename)
        self.expect_signature = 'BAMC'


        self.envelope_desc = (
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

    def decode_file (self):
        self.decode_envelope ()
        data = self.stream.decode_blob (0x0C)

        self.stream.close ()
        self.stream = CompressedStream (data)

        BAM_Format.decode_file (self)

    def print_file (self):
        self.print_envelope ()
        BAM_Format.print_file (self)

    def decode_envelope (self):
        self.envelope = {}
        self.decode_by_desc (0x0000, self.envelope_desc, self.envelope)
        
    def print_envelope (self):
        self.print_by_desc (self.envelope, self.envelope_desc)
        


# assume frame data is always RLE encoded
BAM_Format.default_options['bam_force_rle'] = 1

# decode and load frame data
BAM_Format.default_options['bam_decode_frame_data'] = 1
BAM_Format.default_options['bam_print_frame_bitmap'] = 1
BAM_Format.default_options['bam_print_palette'] = 1


register_format ('BAM', 'V1', BAM_Format)
register_format ('BAMC', 'V1  ', BAMC_Format)
