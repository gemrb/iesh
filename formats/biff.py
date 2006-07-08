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

# RCS: $Id: biff.py,v 1.3 2006/07/08 14:29:26 edheldil Exp $

import gzip
from format import Format, register_format

class BIFF_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'BIFF'

        self.file_list = []
        self.tileset_list = []

        self.header_desc = (
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
        

        self.file_record_desc = (
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
            
            { 'key': 'unknown',
              'type': 'WORD',
              'off': 0x000E,
              'label': '???' },
            )

        self.tileset_record_desc = (
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

    def decode_file (self):
        self.decode_header ()

        off = self.header['files_offset']
        for i in range (self.header['num_of_files']):
            obj = {}
            self.decode_file_record (off, obj)
            self.file_list.append (obj)
            off = off + 16

        for i in range (self.header['num_of_tilesets']):
            obj = {}
            self.decode_tileset_record (off, obj)
            self.tileset_list.append (obj)
            off = off + 20


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.file_list:
            print 'File #%d' %i
            self.print_file_record (obj)
            i = i + 1
            
        i = 0
        for obj in self.tileset_list:
            print 'Tileset #%d' %i
            self.print_tileset_record (obj)
            i = i + 1


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_file_record (self, offset, obj):
        self.decode_by_desc (offset, self.file_record_desc, obj)
        
    def print_file_record (self, obj):
        self.print_by_desc (obj, self.file_record_desc)


    def decode_tileset_record (self, offset, obj):
        self.decode_by_desc (offset, self.tileset_record_desc, obj)
        
    def print_tileset_record (self, obj):
        self.print_by_desc (obj, self.tileset_record_desc)



    def get_ntset_data (self, obj):
        obj['data'] = self.stream.decode_blob (obj['data_offset'], obj['data_size'])

    def get_tileset_data (self, obj):
        # FIXME: also add bytes for the TIS header
        obj['data'] = self.stream.decode_blob (obj['data_offset'], obj['tile_size'] * obj['tile_cnt'])


    def get_file_data (self, obj):
        if obj.has_key ('tile_cnt'):
            return self.get_tileset_data (obj)
        else:
            return self.get_ntset_data (obj)


    def save_file_data (self, filename, obj):
        self.get_file_data (obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()
        

class BIFC_V1_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'BIF '

        self.header_desc = (
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

    def decode_file (self):
        self.decode_header ()

        self.decode_by_desc (0x000c + self.header['filename_len'], (self.header_desc[4], ), self.header)
        self.decode_by_desc (0x0010 + self.header['filename_len'], ( self.header_desc[5], ), self.header)

        #self.stream.seek (..)
        data = self.stream.decode_blob (0x0014 + self.header['filename_len'], self.header['compressed_size'])
        self.data = gzip.zlib.decompress (data)


    def print_file (self):
        self.print_header ()


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        



register_format ('BIFF', 'V1', BIFF_Format)
register_format ('BIF ', 'V1.0', BIFC_V1_Format)
