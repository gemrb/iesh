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

# RCS: $Id: format.py,v 1.1 2005/03/02 20:44:23 edheldil Exp $

import os.path
import re
import string
import struct

from plugins import core

 
PAGE_SIZE = 4096

TICK_SIZE = 100
TACK_SIZE = 5000

def ResolveFilePath (filename):
    if os.path.isfile (filename):
        return filename

    


class Format:
    def __init__ (self, filename):
        self.header_size = 0
        self.bitmask_cache = {}

        self.options = {}

        self.options['debug_decode'] = 0

        self.open_file (filename)

    def open_file (self, filename):
        self.fh = open (filename, "r")        
        self.offset = 0

    def close_file (self):
        self.fh.close ()

    def get_char (self, offset):
        self.fh.seek (offset)
        return self.fh.read (1)

    def decode_word (self, offset):
        self.fh.seek (offset)
        v = self.fh.read (2)
        return struct.unpack ('H', v)[0]

    def decode_dword (self, offset):
        self.fh.seek (offset)
        v = self.fh.read (4)
        return struct.unpack ('I', v)[0]

    def decode_sized_string (self, offset, size):
        self.fh.seek (offset)
        v = self.fh.read (size)
        return struct.unpack ('%ds' %size, v)[0]

    def decode_asciiz_string (self, off):
        s = ''
        
        while 1:
            c = self.get_char (off)
            if c == '\0': break
            s = s + c
            off = off + 1
            
        return s

    def decode_resref (self, off):
        return self.decode_sized_string (off, 8)

    def decode_blob (self, offset, size):
        self.fh.seek (offset)
        return self.fh.read (size)



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

            mask = 0
            for i in range (bl, bh + 1):
                mask = mask | (1 << i)

            #print "MASK: 0x%08x\n" %mask

            self.bitmask_cache[bits] = (mask, bl)
            return mask, bl


#            { 'key': '', 'type': '', 'off': 0x00, 'label': '' },

    def decode_by_desc (self, offset, desc, obj):
        for d in desc:
            key = d['key']
            type = d['type']
            local_offset = d['off']

            if self.options['debug_decode']:
                print d

            if type == 'BYTE':
                value = ord (self.get_char (offset + local_offset))
            elif type == 'CTLTYPE':
                value = ord (self.get_char (offset + local_offset))
            elif type == 'WORD':
                value = self.decode_word (offset + local_offset)
            elif type == 'DWORD':
                value = self.decode_dword (offset + local_offset)
            elif type == 'CTLID':
                value = self.decode_dword (offset + local_offset)
            elif type == 'RGBA':
                value = self.decode_dword (offset + local_offset)
            elif type == 'STR2':
                value = self.decode_sized_string (offset + local_offset, 2)
            elif type == 'STR4':
                value = self.decode_sized_string (offset + local_offset, 4)
            elif type == 'STR32':
                value = self.decode_sized_string (offset + local_offset, 32)
            elif type == 'RESREF':
                value = self.decode_resref (offset + local_offset)
                value = string.translate (value, core.slash_trans, '\x00')
            elif type == 'STRREF':
                value = self.decode_dword (offset + local_offset)
            elif type == 'RESTYPE':
                value = self.decode_word (offset + local_offset)
            elif type == 'STROFF':
                stroff = self.decode_dword (offset + local_offset)
                value = self.decode_asciiz_string (stroff)
                value = string.translate (value, core.slash_trans, '\x00')
            elif type == 'BYTES':
                value = self.decode_blob (offset + local_offset, d['size'])
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

            if self.options['debug_decode']:
                self.print_date_by_desc (obj, d)

                
    def print_by_desc (self, obj, desc):
        for d in desc:
            self.print_date_by_desc (obj, d)
        print

    def print_date_by_desc (self, obj, d):
        key = d['key']
        type = d['type']
        label = d['label']

        try: enum = d['enum']
        except: enum = None

        try: mask = d['mask']
        except: mask = None

        value = obj[key]
        value2 = ''

        if type == 'RESTYPE':
            try: value2 = '(' + core.restype_hash[value] + ')'
            except: pass
        elif type == 'CTLTYPE':
            try: value2 = '(' + ctltype_hash[value] + ')'
            except: pass
        elif type == 'CTLID':
            try: value2 = '(' + '0x%08x' %value + ')'
            except: pass
        elif type == 'STRREF' and core.strrefs:
            try: value2 = '(' + core.strrefs.strref_list[value]['string'] + ')'
            except: pass
        elif type == 'RGBA':
            try: value2 = '(' + '%08x' %value + ')'
            except: pass
        elif enum != None:
            try: value2 = '(' + enum[value] + ')'
            except: pass
        elif mask != None:
            value2 = '(' + string.join (map (lambda m, mask=mask: mask[m], filter (lambda m, v=value: (m & v) == m, mask.keys ())), '|') + ')'

        print label + ':', value, value2


ctltype_hash = {
    0 : 'button/pixmap',
    2 : 'slider',
    3 : 'textedit',
    5 : 'textarea',
    6 : 'label?',
    7 : 'scrollbar',
    }


def register_format (signature, version, klass):
    #core.formats[(signature, version)] = klass
    core.formats[signature] = klass
