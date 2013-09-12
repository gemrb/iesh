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



import sys

from infinity.format import Format, register_format
from infinity.image import Image


class WAVC_Format (Format, Image):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off': 0x0004,
              'label': 'Version' },
            
            { 'key': 'uncompressed_size',
              'type': 'DWORD',
              'off':0x0008,
              'label': 'Uncompressed file size'},
            
            { 'key': 'compressed_size',
              'type': 'DWORD',
              'off':0x000C,
              'label': 'Compressed file size'},
            
            { 'key': 'data_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Data offset'},

            { 'key': 'channels',
              'type': 'WORD',
              'off': 0x0014,
              'label': 'Channels'},

            { 'key': 'bits_per_sample',
              'type': 'WORD',
              'off': 0x0016,
              'label': 'Bits per sample'},

            { 'key': 'sample_rate',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'Sample rate'},

            { 'key': 'unused_1a',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'Unused, usually 0x777e'},

            { 'key': 'acm_header',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'ACM header (0x97280301)'},
            )



    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'WAVC'


    def read (self, stream):
        self.read_header (stream)
        self.acm = stream.read_blob(self.header['data_off'], self.header['compressed_size'])

    def printme (self):
        self.print_header ()



register_format ('WAVC', 'V1.0', WAVC_Format)
