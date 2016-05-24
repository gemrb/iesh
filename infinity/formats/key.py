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


import re
import sys

from infinity import core
from infinity.format import Format, register_format

class KEY_Format (Format):
    header_desc = (
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


    bif_record_desc = (
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
              'mask': { 0x01: 'data',
                        0x02: 'cache',
                        0x04: 'CD1',
                        0x08: 'CD2',
                        0x10: 'CD3',
                        0x20: 'CD4',
                        0x40: 'CD5',
                        0x80: 'CD6' },
              'label': 'BIF location' },
            )

    resref_record_desc = (
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

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'KEY'

        self.bif_list = []
        self.bif_hash = {}

        self.resref_list = []
        self.resref_hash = {}

        # when set to some number, read that number of resources at most
        #self.options['max_read_bifs'] = None


    def read (self, stream):
        self.read_header (stream)

        off = self.header['bif_offset']
        bif_record_size = self.get_struc_size (self.bif_record_desc)
        for i in range (self.header['num_of_bifs']):
            obj = {}
            self.read_bif_record (stream, off, obj)
            self.bif_list.append (obj)
            self.bif_hash[obj['file_name']] = obj
            off = off + bif_record_size

        off = self.header['resref_offset']
        max_read_resrefs = self.header['num_of_resrefs']
        if self.get_option ('format.key.max_read_resrefs'):
            max_read_resrefs = min (max_read_resrefs, self.get_option ('format.key.max_read_resrefs'))

        resref_record_size = self.get_struc_size (self.resref_record_desc)
        tick_size = self.get_option ('format.key.tick_size')
        tack_size = self.get_option ('format.key.tack_size')
        for i in range (max_read_resrefs):
            #if i == 1000:
            #    break

            obj = {}
            self.read_resref_record (stream, off, obj)
            self.resref_list.append (obj)
            obj['file_name'] = self.bif_list[obj['locator_src_ndx']]
            self.resref_hash[obj['resref_name']] = obj
            off = off + resref_record_size

            if not (i % tick_size):
                sys.stdout.write('.')
                if not (i % tack_size):
                    sys.stdout.write('%d' %i)
                sys.stdout.flush ()
        print()

    def write (self, stream):
        # FIXME: STROFF is missing
        header_size = self.get_struc_size (self.header_desc)
        bif_record_size = self.get_struc_size (self.bif_record_desc)
        resref_record_size = self.get_struc_size (self.resref_record_desc)

        self.header['num_of_bifs'] = len (self.bif_list)
        self.header['num_of_resrefs'] = len (self.resref_list)
        self.header['bif_offset'] = header_size
        self.header['resref_offset'] = header_size + len (self.bif_list) * bif_record_size

        self.write_struc (stream, 0x0000, self.header_desc, self.header)

        off2 = self.header['bif_offset']
        for obj in self.bif_list:
            self.write_struc (stream, off2, self.bif_record_desc, obj)
            off2 += bif_record_size

        off2 = self.header['resref_offset']
        for obj in self.resref_list:
            self.write_struc (stream, off2, self.resref_record_desc, obj)
            off2 += resref_record_size


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.bif_list:
            print('#%d' %i)
            self.print_bif_record (obj)
            i = i + 1

        i = 0
        for obj in self.resref_list:
            print('#%d' %i)
            self.print_resref_record (obj)
            i = i + 1


    def read_bif_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.bif_record_desc, obj)

    def print_bif_record (self, obj):
        self.print_struc (obj, self.bif_record_desc)


    def read_resref_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.resref_record_desc, obj)

    def print_resref_record (self, obj):
        self.print_struc (obj, self.resref_record_desc)




    def get_bif_by_name_re (self, name):
        rx = re.compile (name)
        return filter (lambda s, rx=rx: rx.search (s['file_name']), self.bif_list)


    def get_resref_by_file_index (self, index):
        return filter (lambda s, i=index: s['locator_src_ndx'] == i, self.resref_list)

    def get_resref_by_name_re (self, name):
        rx = re.compile (name)
        return filter (lambda s, rx=rx: rx.search (s['resref_name']), self.resref_list)

    def get_resref_by_name (self, name):
        return filter (lambda s, name=name.upper (): s['resref_name'].upper () == name, self.resref_list)

    def get_resref_by_type (self, type):
        return filter (lambda s, type=type: s['type'] == type, self.resref_list)

register_format (KEY_Format, signature='KEY V1  ', extension='KEY', name='KEY')
