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

# RCS: $Id: key.py,v 1.1 2005/03/02 20:44:23 edheldil Exp $

import re
import sys
from format import Format, register_format, TICK_SIZE, TACK_SIZE

class KEY_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'KEY'

        self.bif_list = []
        self.bif_hash = {}

        self.resref_list = []
        self.resref_hash = {}

        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off': 0x0004,
              'label': 'Version'},
            
            { 'key': 'num_of_bifs',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of BIFs'},
            
            { 'key': 'num_of_resrefs',
              'type': 'DWORD',
              'off': 0x000C,
              'label': '# of resref entries'},
            
            { 'key': 'bif_offset',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'First BIF offset'},
            
            { 'key': 'resref_offset',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'First resref offset'},
            )
        

        self.bif_record_desc = (
            { 'key': 'file_len',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'BIF file len' },
            
            { 'key': 'file_name',
              'type': 'STROFF',
              'off': 0x0004,
              'label': 'BIF file name' },
            
            { 'key': 'file_name_offset',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'BIF file name offset' },
            
            { 'key': 'file_name_len',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'BIF file name len' },
            
            { 'key': 'location',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'BIF location' },
            )

        self.resref_record_desc = (
            { 'key': 'resref_name',
              'type': 'RESREF',
              'off': 0x0000,
              'label': 'resref name' },
            
            { 'key': 'type',
              'type': 'RESTYPE',
              'off': 0x0008,
              'label': 'resref type' },
            
            { 'key': 'locator',
              'type': 'DWORD',
              'off': 0x000A,
              'label': 'resref locator' },
            
            { 'key': 'locator_src_ndx',
              'type': 'DWORD',
              'off': 0x000A,
              'bits': '31-20',
              'label': 'resref locator (source index)' },
            
            { 'key': 'locator_tset_ndx',
              'type': 'DWORD',
              'off': 0x000A,
              'bits': '19-14',
              'label': 'resref locator (tileset index)' },
            
            { 'key': 'locator_ntset_ndx',
              'type': 'DWORD',
              'off': 0x000A,
              'bits': '13-0',
              'label': 'resref locator (non-tileset index)' },
            )

    def decode_file (self):
        self.decode_header ()

        off = self.header['bif_offset']
        for i in range (self.header['num_of_bifs']):
            obj = {}
            self.decode_bif_record (off, obj)
            self.bif_list.append (obj)
            self.bif_hash[obj['file_name']] = obj
            off = off + 12

        off = self.header['resref_offset']
        for i in range (self.header['num_of_resrefs']):
            #if i == 1000:
            #    break
            
            obj = {}
            self.decode_resref_record (off, obj)
            self.resref_list.append (obj)
            obj['file_name'] = self.bif_list[obj['locator_src_ndx']]
            self.resref_hash[obj['resref_name']] = obj
            off = off + 14

            if not (i % TICK_SIZE):
                sys.stdout.write('.')
                if not (i % TACK_SIZE):
                    sys.stdout.write('%d' %i)
                sys.stdout.flush ()
        print

    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.bif_list:
            print '#%d' %i
            self.print_bif_record (obj)
            i = i + 1
            
        i = 0
        for obj in self.resref_list:
            print '#%d' %i
            self.print_resref_record (obj)
            i = i + 1


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)

        
    def decode_bif_record (self, offset, obj):
        self.decode_by_desc (offset, self.bif_record_desc, obj)
        
    def print_bif_record (self, obj):
        self.print_by_desc (obj, self.bif_record_desc)


    def decode_resref_record (self, offset, obj):
        self.decode_by_desc (offset, self.resref_record_desc, obj)
        
    def print_resref_record (self, obj):
        self.print_by_desc (obj, self.resref_record_desc)




    def get_bif_by_name_re (self, name):
        rx = re.compile (name)
        return filter (lambda s, rx=rx: rx.search (s['file_name']), self.bif_list)


    def get_resref_by_file_index (self, index):
        return filter (lambda s, i=index: s['locator_src_ndx'] == i, self.resref_list)

    def get_resref_by_name_re (self, name):
        rx = re.compile (name)
        return filter (lambda s, rx=rx: rx.search (s['resref_name']), self.resref_list)
    
register_format ('KEY', 'V1', KEY_Format)
