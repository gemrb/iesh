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

# RCS: $Id: tlk.py,v 1.1 2005/03/02 20:44:23 edheldil Exp $

import re
import string
import sys

from format import Format, register_format, TICK_SIZE, TACK_SIZE

class TLK_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'TLK'

        self.strref_list = []

        

        t_cp1250 = '·ËÔÈÏÌÚÛ¯öù˙˘˝û¡»œ…ÃÕ“”ÿäç⁄Ÿ›é'
        t_iso8859_2 = '·ËÔÈÏÌÚÛ¯πª˙˘˝æ¡»œ…ÃÕ“”ÿ©´⁄Ÿ›Æ'

        self.xlat = string.maketrans (t_cp1250, t_iso8859_2)
        
        self.header_desc = (
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
        

        self.strref_record_desc = (
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


    def decode_file (self):
        self.decode_header ()

        off = 0x0012
        for i in range (self.header['num_of_strrefs']):
            #if i == 3000:
            #    break
            
            obj = {}
            self.decode_strref_record (off, obj)
            self.strref_list.append (obj)
            off = off + 26

            if not (i % TICK_SIZE):
                sys.stdout.write('.')
                if not (i % TACK_SIZE):
                    sys.stdout.write('%d' %i)
                sys.stdout.flush ()
        print


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.strref_list:
            print '#%d' %i
            self.print_strref_record (obj)
            i = i + 1


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_strref_record (self, offset, obj):
        self.decode_by_desc (offset, self.strref_record_desc, obj)
        obj['string'] = string.translate (self.decode_sized_string (self.header['string_offset'] + obj['string_offset'], obj['string_len']), self.xlat)
        
    def print_strref_record (self, obj):
        self.print_by_desc (obj, self.strref_record_desc)



    def get_strref_by_str_re (self, text):
        rx = re.compile (text)
        return filter (lambda s, rx=rx: rx.search (s['string']), self.strref_list)

        
register_format ('TLK', 'V1', TLK_Format)
