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

from __future__ import print_function

import struct
import sys
import PIL

from infinity.format import Format, register_format
from infinity.stream import CompressedStream
from infinity.imagesequence import ImageSequence


class BAM_Format (Format, ImageSequence):
    header_desc = (
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


    frame_desc = (
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Frame width'},

            { 'key': 'height',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Frame height'},

            { 'key': 'x',
              'type': 'WORD',
              'off': 0x0004,
              'label': 'Frame anchor X'},

            { 'key': 'y',
              'type': 'WORD',
              'off': 0x0006,
              'label': 'Frame anchor Y'},

            { 'key': 'uncompressed',
              'type': 'DWORD',
              'off': 0x0008,
              'bits': '31-31',
              'label': 'Uncompressed (0=RLE)'},

            { 'key': 'frame_data_off',
              'type': 'DWORD',
              'off': 0x0008,
              'bits': '30-0',
              'label': 'Frame data offset'},
            )

    cycle_desc = (
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

    palette_entry_desc = (
            { 'key': 'b',
              'type': 'BYTE',
              'off': 0x0000,
              'label': 'R'},

            { 'key': 'g',
              'type': 'BYTE',
              'off': 0x0001,
              'label': 'G'},

            { 'key': 'r',
              'type': 'BYTE',
              'off': 0x0002,
              'label': 'B'},

            { 'key': 'a',
              'type': 'BYTE',
              'off': 0x0003,
              'label': 'A'},
            )

    frame_lut_entry_desc = (
            { 'key': 'frame',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Frame'},
            )


    def __init__ (self):
        Format.__init__ (self)
        ImageSequence.__init__ (self)
        self.expect_signature = 'BAM'

        self.frame_list = []
        self.cycle_list = []
        self.palette_entry_list = []
        self.frame_lut = None

    def read (self, stream):
        self.read_header (stream)

        off = self.header['frame_off']
        for i in range (self.header['frame_cnt']):
            obj = {}
            self.read_frame (stream, off, obj)
            self.frame_list.append (obj)
            off = off + 12

        for i in range (self.header['cycle_cnt']):
            obj = {}
            self.read_cycle (stream, off, obj)
            self.cycle_list.append (obj)
            off = off + 4

        self.read_palette (stream, self.header['palette_off'])

        #if self.get_option ('format.bam.decode_frame_data'):
        #    for obj in self.frame_list:
        #        self.frame_to_rgba (obj)
        return self


    def write (self,  stream):
        # FIXME: incomplete
        frame_size = self.get_struc_size (self.frame_desc)
        cycle_size = self.get_struc_size (self.cycle_desc)

        # FIXME: conver pixels

        self.header['frame_cnt'] = len (self.frame_list)
        self.header['cycle_cnt'] = len (self.cycle_list)
        self.header['frame_off'] = self.get_struc_size (self.header_desc)
        self.header['palette_off'] = self.header['frame_off'] + frame_size * len (self.frame_list) + cycle_size * len (self.cycle_list)
        self.header['frame_lut_off'] = self.header['palette_off'] + 4 * 256

        # NOTE: if self.frame_lut is None, we construct a new one from frames in cycles.
        #   If it is not None, we assume the LUT has already been constructed and that
        #   the frame_cnt and frame_lut_ndx data are valid as well
        if self.frame_lut is  None:
            self.frame_lut = []
            for obj in self.cycle_list:
                obj['frame_cnt'] = len (obj['frame_list'])
                obj['frame_lut_ndx'] = len (self.frame_lut)
                self.frame_lut.extend (obj['frame_list'])

        frame_data_off = self.header['frame_lut_off'] + 2 * len (self.frame_lut)

        self.write_header (stream)

        off = self.header['frame_off']
        off2 = frame_data_off

        for obj in self.frame_list:
            # FIXME: RLE is encoded in the offset
            obj['frame_data_off'] = off2
            self.write_struc (stream, off, self.frame_desc, obj)
            # FIXME: rle
            off2 += self.write_frame_data (stream, off2, obj)
            off += frame_size

        for obj in self.cycle_list:
            self.write_struc (stream, off, self.cycle_desc, obj)
            off += cycle_size

        for obj in self.palette_entry_list:
            self.write_struc (stream, off, self.palette_entry_desc, obj)
            off += 4 # FIXME

        for l in self.frame_lut:
            stream.write_word (l,  off)
            off += 2



    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.frame_list:
            print('Frame #%d' %i)
            self.print_frame (obj)
            i = i + 1

        i = 0
        for obj in self.cycle_list:
            print('Cycle #%d' %i)
            self.print_cycle (obj)
            i = i + 1

        if self.get_option ('format.bam.print_palette'):
            self.print_palette ()


    def read_frame (self, stream, offset, obj):
        self.read_struc (stream, offset, self.frame_desc, obj)

        if self.get_option ('format.bam.decode_frame_data'):
            if obj['uncompressed']:
                self.read_frame_data (stream, obj)
            else:
                self.read_rle_frame_data (stream, obj)


    def print_frame (self, obj):
        self.print_struc (obj, self.frame_desc)

        if self.get_option ('format.bam.print_frame_bitmap'):
            self.print_bitmap (obj)
            print()

    def read_cycle (self, stream, offset, obj):
        self.read_struc (stream, offset, self.cycle_desc, obj)
        obj['frame_list'] = []

        off2 = self.header['frame_lut_off'] + 2 * obj['frame_lut_ndx']
        obj2 = {}
        for i in range (obj['frame_cnt']):
            self.read_struc (stream, off2, self.frame_lut_entry_desc, obj2)
            obj['frame_list'].append (obj2['frame'])
            obj['frames'] = obj['frames'] + str(obj2['frame']) + ' '
            off2 = off2 + 2

    def print_cycle (self, obj):
        self.print_struc (obj, self.cycle_desc)


    def read_palette (self, stream, offset):
        transp_color = None

        for i in range (256):
            obj = {}
            self.read_struc (stream, offset, self.palette_entry_desc, obj)
            self.palette_entry_list.append (obj)

            if transp_color is None and obj['r'] == 0 and obj['g'] == 255 and obj['b'] == 0:
                transp_color = i

            offset = offset + 4

        if transp_color is None:
            transp_color = 0
        self.header['transp_color_ndx'] = transp_color


    def print_palette (self):
        i = 0
        for obj in self.palette_entry_list:
            print("%3d: %3d %3d %3d %3d (#%02x%02x%02x%02x)" %(i, obj['r'], obj['g'], obj['b'], obj['a'], obj['r'], obj['g'], obj['b'], obj['a']))
            i = i + 1


    def read_frame_data (self, stream, obj):
        size = obj['width'] * obj['height']
        bin_data = stream.read_blob (obj['frame_data_off'], size)
        obj['frame_data'] = struct.unpack ('%dB' %size, bin_data)


    def read_rle_frame_data (self, stream, obj):
        off = obj['frame_data_off']
        size = obj['width'] * obj['height']
        compressed_color = self.header['comp_color_ndx']

        data = []
        while len (data) < size:
            pix = struct.unpack ('B', stream.get_char (off))[0]
            if pix == compressed_color:
                off = off + 1
                cnt = struct.unpack ('B', stream.get_char (off))[0]
                # FIXME: that's strange, only one color is compressed?
                data.extend ([compressed_color] * (cnt + 1))
#                for j in range (cnt + 1):
#                    data.append (compressed_color)
            else:
                data.append (pix)

            off = off + 1

        obj['frame_data'] = data


    def get_frame_lol (self):
        return [ self.frame_list[:] ]

    def frame_to_image (self, obj):
        transparent = self.header['transp_color_ndx']
        ndx = 0
        data = []
        for i in range (obj['height']):
            for j in range (obj['width']):
                color = obj['frame_data'][ndx]
                p = self.palette_entry_list[color]
                pix = '%c%c%c%c' %(p['r'], p['g'], p['b'], (255, 0)[color == transparent])
                data.append(pix)
                ndx = ndx + 1

        img = PIL.Image.frombytes ('RGBA', (obj['width'], obj['height']), ''.join(data), "raw", 'RGBA', 0, 1)
        img.x = 0
        img.y = 0

        obj['image'] = img


    def write_frame_data (self, stream, off, obj):
        #data = obj['frame_data']
        # FIXME: allow writing uncompressed
        data = self.compress_frame_data (obj)
        data = struct.pack ('%dB' %len (data), *data)
        stream.write_blob (data,  off)
        return len (data)



    def find_compressed_color (self, stream, off, obj):
        """Find color which benefits most from compression"""
        comp_data = []
        last_pixel = obj['frame_data'][0]
        count = 0

        for pixel in obj['frame_data']:
            if pixel == last_pixel:
                count += 1
            elif count < min_count:
                ### FIXME: count!
                # FIXME: split if count > 255
                comp_data.extend ([last_pixel] * count)
                last_pixel = pixel
                count = 1
            else:
                comp_data.extend ([])

        data = struct.pack ('%dB' %len (obj['frame_data']), *obj['frame_data'])
        stream.write_blob (data,  off)
        return len (data)


    def compress_frame_data (self, obj):
        comp_data = []
        count = 0
        compressed_color = self.header['comp_color_ndx']
        # FIXME: check if orig IE BAMs do not split compressed run on pixel row end
        for pixel in obj['frame_data']:
            if pixel != compressed_color:
                if count > 0:
                    comp_data.append (compressed_color)
                    comp_data.append (count - 1)
                    count = 0
                comp_data.append(pixel)

            else:
                count += 1
                if count == 256:
                    comp_data.append (compressed_color)
                    comp_data.append (count - 1)
                    count = 0

        if count > 0:
            comp_data.append (compressed_color)
            comp_data.append (count - 1)


        return comp_data


    def print_frame_data (self, obj):
        ndx = 0
        for i in range (obj['height']):
            for j in range (obj['width']):
                print('%3d' %obj['frame_data'][ndx], end=' ')
                ndx = ndx + 1
            print()
        print()


class BAMC_Format (BAM_Format):
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
        BAM_Format.__init__ (self)
        self.expect_signature = 'BAMC'


    def read (self, stream):
        self.read_envelope (stream)
        data = stream.read_blob (0x0C)

        #self.stream.close ()
        stream = CompressedStream ().open (data)

        return BAM_Format.read (self, stream)

    def write (self, stream):
        tmpstream = CompressedStream ().open (data, 'wb')
        self.write (tmpstream)
        data = tmpstream.data
        # self.envelope['uncompressed_size'] = ...
        self.write_envelope (stream)
        stream.write_blob (data)

    def printme (self):
        self.print_envelope ()
        BAM_Format.printme (self)

    def read_envelope (self, stream):
        self.envelope = {}
        self.read_struc (stream, 0x0000, self.envelope_desc, self.envelope)

    def write_envelope (self, stream):
        self.write_struc (stream, 0x0000, self.envelope_desc, self.envelope)

    def print_envelope (self):
        self.print_struc (self.envelope, self.envelope_desc)





register_format (BAM_Format, signature='BAM V1  ')
register_format (BAMC_Format, signature='BAMCV1  ')
