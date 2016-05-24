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


class SAV_Format (Format):
    header_desc = (
          { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

          { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
          )

    file_desc = (
            { 'key': 'filename',
              'type': 'STRSIZED',
              'off': 0x0000,
              'label': 'Filename'},
            )

    file2_desc = (
            { 'key': 'uncompressed_size',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Uncompressed file size'},

            { 'key': 'compressed_size',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Compressed file size'},

#            { 'key': 'data_offset',
#              'type': '_BYTE',
#              'off': 0x0000,
#              'label': 'Data offset'},
#
#            { 'key': 'data',
#              'type': '_BYTE',
#              'off': 0x000C,
#              'label': 'Data'},

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'SAV'

        self.file_list = []


    def read (self, stream):
        self.read_header (stream)

        off = self.get_struc_size (self.header_desc)

        while True:
            obj = {}
            try:
                self.read_struc (stream, off, self.file_desc, obj)
            except:
                # Assume all exception to be struct.error due to eof
                break
            off += len (obj['filename']) + 1
            self.read_struc (stream, off, self.file2_desc, obj)
            off += self.get_struc_size (self.file2_desc)
            obj['data_offset'] = off
            off += obj['compressed_size']

            self.file_list.append (obj)

        if self.get_option ('format.sav.read_data'):
            self.read_all_data (stream)

    def write (self, stream):
        # FIXME: rather do reset_struc()
        self.header = {}
        self.header['signature'] = 'SAV '
        self.header['version'] = 'V1.0'
        self.write_header (stream)
        off = self.get_struc_size (self.header_desc)

        for obj in self.file_list:
            self.write_struc (stream, off, self.file_desc, obj)
            off += len (obj['filename']) + 1
            self.write_struc (stream, off, self.file2_desc, obj)
            off += self.get_struc_size (self.file2_desc)
            stream.write_blob (obj['data'], off, obj['compressed_size'])
            off += obj['compressed_size']


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.file_list:
            print('File #%d' %i)
            self.print_struc (obj, self.file_desc)
            self.print_struc (obj, self.file2_desc)
            i = i + 1

    def append_file (self, filename, data):
        obj = {}
        obj['filename'] = filename
        obj['uncompressed_size'] = len (data)
        data = gzip.zlib.compress (data)
        obj['compressed_size'] = len (data)
        obj['data'] = data
        self.file_list.append (obj)





    def read_all_data (self, stream):
        for obj in self.file_list:
            self.read_data (stream, obj)
            # FIXME: uncompress

    def read_data (self, stream, obj):
        data = stream.read_blob (obj['data_offset'], obj['compressed_size'])
        stream2 = CompressedStream ().open (data)
        obj['data'] = stream2.read_blob (0, obj['uncompressed_size'])
        return obj['data']

    # FIXME: there should be a fn, which would just return a stream. That stream
    #   would (if read) on-demand read the original file and uncompress it on the fly
    #   to minimize memory consumption

    # FIXME: the following API is ugly

    def get_file_data (self, stream, obj):
        # avoid rereading already read data and also do not replace data read from uncompressed stream
        #   in the case of a CBF file
        if obj.has_key ('data'):
            return obj['data']

        return self.read_data (stream, obj)

    # FIXME: this is ugly

    def save_file_data (self, stream, filename, obj):
        # FIXME: does not work with CBF files and the outer stream
        self.get_file_data (stream, obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()





register_format (SAV_Format, signature='SAV V1.0', extension='SAV', name=('SAV', 'SAVE'))
