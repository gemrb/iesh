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

# RCS: $Id: biff.py,v 1.1 2005/03/02 20:44:22 edheldil Exp $

from format import Format, register_format

class BIFF_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'BIFF'

        self.file_list = []

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
            
            { 'key': 'num_of_tsets',
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

        self.res_record_desc = (
            { 'key': 'res_name', 'type': 'STRREF', 'off': 0x0000, 'label': 'res name strref' },
            { 'key': 'type', 'type': 'WORD', 'off': 0x0008, 'label': 'res type' },
            { 'key': 'locator', 'type': 'DWORD', 'off': 0x000A, 'label': 'res locator' },
            { 'key': 'locator_src_ndx', 'type': 'DWORD', 'off': 0x000A, 'bits': '31-20', 'label': 'res locator (source index)' },
            { 'key': 'locator_tset_ndx', 'type': 'DWORD', 'off': 0x000A, 'bits': '19-14', 'label': 'res locator (tileset index)' },
            { 'key': 'locator_ntset_ndx', 'type': 'DWORD', 'off': 0x000A, 'bits': '13-0', 'label': 'res locator (non-tileset index)' },
            )

    def decode_file (self):
        self.decode_header ()

        off = self.header['files_offset']
        for i in range (self.header['num_of_files']):
            obj = {}
            self.decode_file_record (off, obj)
            self.file_list.append (obj)
            off = off + 16

        return
    
        obj = {}
        off = self.header['res_offset']
        for i in range (self.header['num_of_res']):
            self.decode_res_record (off, obj)
            off = off + 14
            print '#%d' %i
            self.print_res_record (obj)

    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.file_list:
            print '#%d' %i
            self.print_file_record (obj)
            i = i + 1
            
        return
    
        for i in range (self.header['num_of_res']):
            self.decode_res_record (off, obj)
            off = off + 14
            print '#%d' %i
            self.print_res_record (obj)


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_file_record (self, offset, obj):
        self.decode_by_desc (offset, self.file_record_desc, obj)
        
    def print_file_record (self, obj):
        self.print_by_desc (obj, self.file_record_desc)


    def decode_res_record (self, offset, obj):
        self.decode_by_desc (offset, self.res_record_desc, obj)
        
    def print_res_record (self, obj):
        self.print_by_desc (obj, self.res_record_desc)



    def get_file_res_data (self, obj):
        obj['data'] = self.decode_blob (obj['data_offset'], obj['data_size'])

    def save_file_res (self, filename, obj):
        self.get_file_res_data (obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()
        
register_format ('BIFF', 'V1', BIFF_Format)
