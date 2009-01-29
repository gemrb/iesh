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
import string
import sys

from infinity import core
from infinity.format import Format, register_format

class TLK_Format (Format):
    
    header_desc = (
        { 'key': 'signature',
          'type': 'STR4',
          'off': 0x0000,
          'label': 'Signature' },
            
        { 'key': 'version',
          'type': 'STR4',
          'off':0x0004,
          'label': 'Version'},
            
        { 'key': 'unknown',
          'type': 'WORD',
          'off': 0x0008,
          'label': '???' },

        { 'key': 'num_of_strrefs',
          'type': 'DWORD',
          'off': 0x000A,
          'label': '# of strref entries'},
            
        { 'key': 'string_offset',
          'type': 'DWORD',
          'off': 0x000E,
          'label': 'First string data offset'},
       )
        

    strref_record_desc = (
        { 'key': 'content_type',
          'type': 'WORD',
          'off': 0x0000,
          'label': 'Content of this entry' },
       
        { 'key': 'sound_resref',
          'type': 'RESREF',
          'off': 0x0002,
          'label': 'Sound resref' },
         
        { 'key': 'volume_variance',
          'type': 'DWORD',
          'off': 0x000A,
          'label': 'Volume variance' },
          
        { 'key': 'pitch_variance',
          'type': 'DWORD',
          'off': 0x000E,
          'label': 'Pitch variance' },
            
        { 'key': 'string_offset',
          'type': 'DWORD',
          'off': 0x0012,
          'label': 'String data rel offset' },

        { 'key': 'string_len',
          'type': 'DWORD',
          'off': 0x0016,
          'label': 'String data size' },

        { 'key': 'string',
          'type': '_STRING',
          'off': 0x0000,
          'label': 'String' },

        )

    def __init__ (self):
        Format.__init__ (self)
        
        self.expect_signature = 'TLK'

        self.strref_list = []
        

    def read (self, stream):
        self.read_header (stream)

        off = 0x0012
            
        if not self.get_option ('format.tlk.decode_strrefs'):
            return
        
        tick_size = core.get_option ('format.tlk.tick_size')
        tack_size = core.get_option ('format.tlk.tack_size')

        for i in range (self.header['num_of_strrefs']):
            
            obj = {}
            self.read_strref_record (stream, off, obj)
            self.strref_list.append (obj)
            off = off + 26

            if not (i % tick_size):
                sys.stdout.write('.')
                if not (i % tack_size):
                    sys.stdout.write('%d' %i)
                sys.stdout.flush ()
        print

    def write (self, stream):
        self.header['num_strings'] = len (self.strref_list)
        self.header['string_offset'] = self.get_struc_size (self.header_desc, self.header) + len (self.strref_list) * self.get_struc_size (self.strref_record_desc, None)
        self.write_struc (stream, 0x0000, self.header_desc, self.header)
        
        strref_offset = self.get_struc_size (self.header_desc, self.header)
        string_offset = 0
        strref_size = self.get_struc_size (self.strref_record_desc, None)
        for strref in self.strref_list:
            # FIXME: possibly test strref type instead
            if len (strref['string']) != 0:
                strref['string_offset'] = string_offset
                stream.write_sized_string (strref['string'], self.header['string_offset'] + string_offset, len (strref['string']))
            else:
                strref['string_offset'] = 0
            self.write_struc (stream, strref_offset, self.strref_record_desc, strref)
            # FIXME: or raw_string ?
            strref_offset += strref_size
            string_offset += len (strref['string'])
        

    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.strref_list:
            print '#%d' %i
            self.print_strref_record (obj)
            i = i + 1


    def read_strref_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.strref_record_desc, obj)
        obj['string'] = stream.read_sized_string (self.header['string_offset'] + obj['string_offset'], obj['string_len'])
        obj['string_raw'] = obj['string']
        if core.lang_trans:
            obj['string'] = string.translate (obj['string'], core.lang_trans)
        
    def print_strref_record (self, obj):
        self.print_struc (obj, self.strref_record_desc)



    def get_strref_by_str_re (self, text):
        rx = re.compile (text)
        return filter (lambda s, rx=rx: rx.search (s['string']), self.strref_list)


        
register_format ('TLK', 'V1', TLK_Format)
