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


import gzip
from infinity.format import Format, register_format
from infinity.stream import CompressedStream


class BIFF_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'num_of_files',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of files'},
            
            { 'key': 'num_of_tilesets',
              'type': 'DWORD',
              'off': 0x000C,
              'label': '# of tilesets'},
            
            { 'key': 'files_offset',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'First file record offset'},
            )
        

    file_record_desc = (
            { 'key': 'locator',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'File resource locator' },
            
            { 'key': 'data_offset',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'File data offset' },
            
            { 'key': 'data_size',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'File data size' },
            
            { 'key': 'type',
              'type': 'RESTYPE',
              'off': 0x000C,
              'label': 'File res type' },
            
            { 'key': 'unknown_0E',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Unknown 0E' },
            )

    tileset_record_desc = (
            { 'key': 'locator',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Tileset resource locator' },
            
            { 'key': 'data_offset',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Tileset data offset' },
            
            { 'key': 'tile_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Number of tiles' },
            
            { 'key': 'tile_size',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Size of tile' },
            
            { 'key': 'type',
              'type': 'RESTYPE',
              'off': 0x0010,
              'label': 'Tileset res type' },

            { 'key': 'unknown_12',
              'type': 'WORD',
              'off': 0x0012,
              'label': 'Unknown 12' },

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'BIFF'

        self.file_list = []
        self.tileset_list = []


    def read (self, stream):
        self.read_header (stream)

        off = self.header['files_offset']
        for i in range (self.header['num_of_files']):
            obj = {}
            self.read_file_record (stream, off, obj)
            self.file_list.append (obj)
            off = off + 16

        for i in range (self.header['num_of_tilesets']):
            obj = {}
            self.read_tileset_record (stream, off, obj)
            self.tileset_list.append (obj)
            off = off + 20

        if self.get_option ('format.biff.read_data'):
            self.read_all_data (stream)

    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.file_list:
            print('File #%d' %i)
            self.print_file_record (obj)
            i = i + 1
            
        i = 0
        for obj in self.tileset_list:
            print('Tileset #%d' %i)
            self.print_tileset_record (obj)
            i = i + 1


    def read_file_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.file_record_desc, obj)
        
    def print_file_record (self, obj):
        self.print_struc (obj, self.file_record_desc)


    def read_tileset_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.tileset_record_desc, obj)
        
    def print_tileset_record (self, obj):
        self.print_struc (obj, self.tileset_record_desc)

    def read_all_data (self, stream):
        for obj in self.file_list:
            self.read_ntset_data (stream, obj)
                
        for obj in self.tileset_list:
            self.read_tileset_data (stream, obj)


    def read_ntset_data (self, stream, obj):
        obj['data'] = stream.read_blob (obj['data_offset'], obj['data_size'])

    def read_tileset_data (self, stream, obj):
        # FIXME: also add bytes for the TIS header
        obj['data'] = stream.read_blob (obj['data_offset'], obj['tile_size'] * obj['tile_cnt'])

    # FIXME: the following API is ugly

    def get_file_data (self, stream, obj):
        # avoid rereading already read data and also do not replace data read from uncompressed stream
        #   in the case of a CBF file
        if obj.has_key ('data'):
            return obj['data']
            
        if obj.has_key ('tile_cnt'):
            return self.read_tileset_data (stream, obj)
        else:
            return self.read_ntset_data (stream, obj)

    # FIXME: this is ugly

    def save_file_data (self, stream, filename, obj):
        # FIXME: does not work with CBF files and the outer stream
        self.get_file_data (stream, obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()
        

class BIFC_V1_Format (BIFF_Format):
    envelope_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
           { 'key': 'filename_len',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Filename length'},
            
           { 'key': 'filename',
              'type': 'STRSIZED',
              'off': 0x0008,
              'label': 'Filename'},
            
           { 'key': 'uncompressed_size',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Uncompressed size'},
            
           { 'key': 'compressed_size',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Compressed size'},
            
             )

    def __init__ (self):
        BIFF_Format.__init__ (self)
        self.expect_signature = 'BIF '

    def read (self, stream):
        self.read_envelope (stream)

        self.read_struc (stream, 0x000C + self.envelope['filename_len'], (self.envelope_desc[4], ), self.envelope)
        self.read_struc (stream, 0x0010 + self.envelope['filename_len'], ( self.envelope_desc[5], ), self.envelope)

        data = stream.read_blob (0x0014 + self.envelope['filename_len'], self.envelope['compressed_size'])
        stream2 = CompressedStream ().open (data)
        res = BIFF_Format.read (self, stream2)
        # read the data with uncompressed stream while we have it
        self.read_all_data (stream2)
        return res
        

    def printme (self):
        self.print_envelope ()
        print()
        BIFF_Format.printme (self)

    def read_envelope (self, stream):
        self.envelope = {}
        self.read_struc (stream, 0x0000, self.envelope_desc, self.envelope)
        
    def print_envelope (self):
        self.print_struc (self.envelope, self.envelope_desc)
        


register_format (BIFF_Format, signature='BIFFV1  ', extension='BIF', name=('BIF', 'BIFF'))
register_format (BIFC_V1_Format, signature='BIF V1.0', extension='CBF', name='CBF')
