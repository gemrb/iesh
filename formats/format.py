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

# RCS: $Id: format.py,v 1.4 2006/07/03 18:15:35 edheldil Exp $

import os.path
import re
import string
import struct
import types

from plugins import core
from stream import Stream, FileStream, ResourceStream
 
PAGE_SIZE = 4096

TICK_SIZE = 100
TACK_SIZE = 5000

def ResolveFilePath (filename):
    if os.path.isfile (filename):
        return filename

    


class Format:
    
    default_options = {}
    
    def __init__ (self, source):
        self.header_size = 0
        self.bitmask_cache = {}
        self.options = {}

        if not isinstance (source, Stream):
            source = FileStream (source)

        self.stream = source
        self.stream.open ()

    def get_masked_bits (self, value, mask, bl):
        return (value & mask) >> bl

    # FIXME: cache it globally ...
    def bits_to_mask (self, bits):
        try:
            return self.bitmask_cache[bits]
        except:
            bh, bl = map (int, string.split (bits, '-'))
            if bl > bh:
                print "warning: bh < bl:", bits
                bh, bl = bl, bh

            mask = 0L
            for i in range (bl, bh + 1):
                mask = mask | (1L << i)

            #print "MASK: 0x%08x\n" %mask

            self.bitmask_cache[bits] = (mask, bl)
            return mask, bl


#            { 'key': '', 'type': '', 'off': 0x00, 'label': '' },

    def decode_by_desc (self, offset, desc, obj):
        for d in desc:
            key = d['key']
            type = d['type']
            local_offset = d['off']

            stream = self.stream

            if self.get_option ('debug_decode'):
                print d

            if type == 'BYTE':
                value = ord (stream.get_char (offset + local_offset))
            elif type == 'CTLTYPE':
                value = ord (stream.get_char (offset + local_offset))
            elif type == 'WORD':
                value = stream.decode_word (offset + local_offset)
            elif type == 'DWORD':
                value = stream.decode_dword (offset + local_offset)
            elif type == 'CTLID':
                value = stream.decode_dword (offset + local_offset)
            elif type == 'RGBA':
                value = stream.decode_dword (offset + local_offset)
            elif type == 'STR2':
                value = stream.decode_sized_string (offset + local_offset, 2)
            elif type == 'STR4':
                value = stream.decode_sized_string (offset + local_offset, 4)
            elif type == 'STR32':
                value = stream.decode_sized_string (offset + local_offset, 32)
            elif type == 'RESREF':
                value = stream.decode_resref (offset + local_offset)
                value = string.translate (value, core.slash_trans, '\x00')
            elif type == 'STRREF':
                value = stream.decode_dword (offset + local_offset)
            elif type == 'RESTYPE':
                value = stream.decode_word (offset + local_offset)
            elif type == 'STROFF':
                stroff = stream.decode_dword (offset + local_offset)
                value = stream.decode_asciiz_string (stroff)
                value = string.translate (value, core.slash_trans, '\x00')
            elif type == 'BYTES':
                value = stream.decode_blob (offset + local_offset, d['size'])
            elif type == '_STRING':
                value = ''
            elif type == '_BYTE':
                value = '?'
            else:
                raise "Unknown data type `%s'" %type
                #value = ''

            if d.has_key ('bits'):
                mask, bl = self.bits_to_mask (d['bits'])
                value = self.get_masked_bits (value, mask, bl)

            obj[key] = value

            if self.get_option ('debug_decode'):
                self.print_date_by_desc (obj, d)

                
    def print_by_desc (self, obj, desc):
        for d in desc:
            self.print_date_by_desc (obj, d)
        print

    def print_date_by_desc (self, obj, d):
        key = d['key']
        rec_type = d['type']
        label = d['label']

        try: enum = d['enum']
        except: enum = None

        try: mask = d['mask']
        except: mask = None

        value = obj[key]
        value2 = ''

        if rec_type == 'RESTYPE':
            try: value2 = '(' + core.restype_hash[value] + ')'
            except: pass
        elif rec_type == 'CTLTYPE':
            try: value2 = '(' + ctltype_hash[value] + ')'
            except: pass
        elif rec_type == 'CTLID':
            try: value2 = '(' + '0x%08x' %value + ')'
            except: pass
        elif rec_type == 'STRREF' and core.strrefs:
            try: value2 = '(' + core.strrefs.strref_list[value]['string'] + ')'
            except: pass
        elif rec_type == 'RGBA':
            try: value2 = '(' + '%08x' %value + ')'
            except: pass
        elif enum != None:
            if type (enum) == types.DictType:
                try: value2 = '(' + enum[value] + ')'
                except: pass

            elif type (enum) == types.StringType:
                if not core.ids.has_key (enum):
                    try:
                        ids = ResourceStream (enum).load_object ()
                        ids.decode_file ()
                        core.ids[enum] = ids
                    except:
                        pass

                try: value2 = '(' + core.ids[enum].ids[value] + ')'
                except: pass
                    
                
        elif mask != None:
            value2 = '(' + string.join (map (lambda m, mask=mask: mask[m], filter (lambda m, v=value: (m & v) == m, mask.keys ())), '|') + ')'

        print label + ':', value, value2


    def set_option_default (key, value):
        Format.default_options[key] = value

    def set_option (self, key, value):
        self.options[key] = value

    def get_option (self, key):
        if self.options.has_key (key):
            return self.options[key]
        elif core.options.has_key (key):
            return core.options[key]
        else:
            return Format.default_options[key]


Format.default_options['debug_decode'] = 0



ctltype_hash = {
    0 : 'button/pixmap',
    2 : 'slider',
    3 : 'textedit',
    5 : 'textarea',
    6 : 'label?',
    7 : 'scrollbar',
    }



def register_format (signature, version, klass):
    core.register_format (signature, version, klass)
