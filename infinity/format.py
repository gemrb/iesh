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


"""
Implements Format, abstract class representing  IE file type.

This modules implements Format, abstract base class 
representing IE file types. This class is futher subclassed 
in infinity.formats package to the various IE file formats
like 2DA, BAM, TLK etc."""

import os.path
import re
import string
import struct
import types

from infinity import core
from infinity.stream import Stream, FileStream, ResourceStream
 

def ResolveFilePath (filename):
    if os.path.isfile (filename):
        return filename

    


class Format (object):
    def __init__ (self):
        self.header_size = 0
        self.bitmask_cache = {}
        self.options = {}


    def read_header (self, stream, desc = None):
        if desc is None:
            self.header = {}
            desc = self.header_desc
        self.read_struc (stream, 0x0000, desc, self.header)

    def write_header (self, stream, desc = None):
        if desc is None:
            desc = self.header_desc
        self.write_struc (stream, 0x0000, desc, self.header)

    def print_header (self, desc = None):
        if desc is None:
            desc = self.header_desc
        self.print_struc (self.header, desc)


    def read_list (self, stream, name,  header = None, desc = None, list = None):
        if desc is None:
            desc = self.__getattribute__ (name + '_desc')
        if list is None:
            list = self.__getattribute__ (name + '_list')
        if header is None:
            header = self.header

        off = header[name + '_off']
        size = self.get_struc_size (desc)
        
        for i in range (header[name + '_cnt']):
            obj = {}
            self.read_struc (stream, off, desc, obj)
            list.append (obj)
            off += size

    def write_list (self, stream, offset, name,  header = None, desc = None, list = None):
        if desc is None:
            desc = self.__getattribute__ (name + '_desc')
        if list is None:
            list = self.__getattribute__ (name + '_list')
        if header is None:
            header = self.header

        header[name + '_off'] = offset
        header[name + '_cnt'] = len (list)
        size = self.get_struc_size (desc)

        for obj in list:
            self.write_struc (stream, offset, desc, obj)
            offset += size

        return offset


    def print_list (self, name, desc = None, list = None):
        if desc is None:
            desc = self.__getattribute__ (name + '_desc')
        if list is None:
            list = self.__getattribute__ (name + '_list')

        i = 0
        for obj in list:
            print name.capitalize () + " #%d:" %i
            self.print_struc (obj, desc)
            i += 1


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


    # { 'key': '', 'type': '', 'off': 0x00, 'label': '' },

    def get_struc_field (self,  desc,  key,  value):
        return None

    def reset_struc (self, desc, obj):
        for d in desc:
            key = d['key']
            type = d['type']
            try:
                value = d['default']
            except:
                if type in ('BYTE', 'WORD', 'DWORD', 'CTLTYPE', 'CTLID', 'RGBA', 'STRREF', 'RESTYPE'):
                    value = 0
                elif type in ('STR2', 'STR4', 'STR8', 'STR32', 'RESREF', 'STRSIZED'):
                    value = ''
                elif type == 'POINT':
                    value = (0, 0)
                elif type == 'RECT':
                    value = (0, 0, 0, 0)
                else:
                    raise Error ("Unknown type")

            # FIXME: bit masks
            obj[key] = value
            
        return obj
            
    def read_struc (self, stream, offset, desc, obj):
        obj['_offset'] = offset
        for d in desc:
            key = d['key']
            type = d['type']
            local_offset = d['off']
            try: count = d['count']
            except: count = 1
            d['count'] = 1
            size = self.get_struc_size ([ d ]) - local_offset
            d['count'] = count

            if self.get_option ('format.debug_read'):
                print d

            for index in range (count):
                #print d, local_offset, key, type, count, index, size
                if type == 'BYTE':
                    value = ord (stream.get_char (offset + local_offset))
                elif type == 'CTLTYPE':
                    value = ord (stream.get_char (offset + local_offset))
                elif type == 'WORD':
                    value = stream.read_word (offset + local_offset)
                elif type == 'DWORD':
                    value = stream.read_dword (offset + local_offset)
                elif type == 'POINT':
                    value0 = stream.read_word (offset + local_offset)
                    value1 = stream.read_word (offset + local_offset + 2)
                    value = (value0, value1)
                elif type == 'RECT':
                    value0 = stream.read_word (offset + local_offset)
                    value1 = stream.read_word (offset + local_offset + 2)
                    value2 = stream.read_word (offset + local_offset + 4)
                    value3 = stream.read_word (offset + local_offset + 6)
                    value = (value0, value1, value2, value3)
                elif type == 'CTLID':
                    value = stream.read_dword (offset + local_offset)
                elif type == 'RGBA':
                    value = stream.read_dword (offset + local_offset)
                elif type == 'STR2':
                    value = stream.read_sized_string (offset + local_offset, 2)
                elif type == 'STR4':
                    value = stream.read_sized_string (offset + local_offset, 4)
                elif type == 'STR8':
                    value = stream.read_sized_string (offset + local_offset, 8)
                elif type == 'STR32':
                    value = stream.read_sized_string (offset + local_offset, 32)
                elif type == 'RESREF':
                    value = stream.read_resref (offset + local_offset)
                    value = string.translate (value, core.slash_trans, '\x00')
                elif type == 'STRREF':
                    value = stream.read_dword (offset + local_offset)
                elif type == 'RESTYPE':
                    value = stream.read_word (offset + local_offset)
                elif type == 'STROFF':
                    str_offset = stream.read_dword (offset + local_offset)
                    str_value = stream.read_asciiz_string (str_offset)
                    str_value = string.translate (str_value, core.slash_trans, '\x00')
                    obj[key + ':offset'] = str_offset
                    # FIXME: ugly
                    #value = (str_offset, str_value)
                    value = str_value
                elif type == 'STRSIZED':
                    length = stream.read_dword (offset + local_offset)
                    # FIXME: asciiz or sized???
                    value = stream.read_asciiz_string (offset + local_offset + 4)
                elif type == 'BYTES':
                    value = stream.read_blob (offset + local_offset, d['size'])
                elif type == '_STRING':
                    value = ''
                elif type == '_BYTE':
                    value = '?'
                else:
                    raise ValueError ("Unknown data type: " + type)
                    #value = ''
    
                if d.has_key ('bits'):
                    mask, bl = self.bits_to_mask (d['bits'])
                    value = self.get_masked_bits (value, mask, bl)
    
                if count > 1:
                    try: obj[key].append (value)
                    except KeyError: obj[key] = [ value ]
                    local_offset += size
                else:
                    obj[key] = value

            if self.get_option ('format.debug_read'):
                self.print_date_by_desc (obj, d)

                
    def print_struc (self, obj, desc):
        for d in desc:
            self.print_date_by_desc (obj, d)
        print

    def write_struc (self, stream, offset, desc, obj):
        for d in desc:
            key = d['key']
            type = d['type']
            local_offset = d['off']

            value = obj[key]
            
            if self.get_option ('format.debug_write'):
                print '%05d' %(offset + local_offset), d, value

            if type == 'BYTE':
                stream.put_char (chr (value), offset + local_offset)
            elif type == 'CTLTYPE':
                stream.put_char (chr (value), offset + local_offset)
            elif type == 'WORD':
                stream.write_word (value, offset + local_offset)
            elif type == 'DWORD':
                stream.write_dword (value, offset + local_offset)
            elif type == 'POINT':
                stream.write_word (value[0], offset + local_offset)
                stream.write_word (value[1], offset + local_offset + 2)
            elif type == 'RECT':
                stream.write_word (value[0], offset + local_offset)
                stream.write_word (value[1], offset + local_offset + 2)
                stream.write_word (value[2], offset + local_offset + 4)
                stream.write_word (value[3], offset + local_offset + 6)
            elif type == 'CTLID':
                stream.write_dword (value, offset + local_offset)
            elif type == 'RGBA':
                stream.write_dword (value, offset + local_offset)
            elif type == 'STR2':
                stream.write_sized_string (value, offset + local_offset, 2)
            elif type == 'STR4':
                stream.write_sized_string (value, offset + local_offset, 4)
            elif type == 'STR8':
                stream.write_sized_string (value, offset + local_offset, 8)
            elif type == 'STR32':
                stream.write_sized_string (value, offset + local_offset, 32)
            elif type == 'RESREF':
                # FIXME: value = string.translate (value, core.slash_trans, '\x00')
                stream.write_resref (value, offset + local_offset)
            elif type == 'STRREF':
                stream.write_dword (value, offset + local_offset)
            elif type == 'RESTYPE':
                stream.write_word (value, offset + local_offset)
            elif type == 'STROFF':
                stream.write_dword (obj[key + ':offset'], offset + local_offset)
                # FIXME: won't work for files starting at non-zero offsets
                # FIXME: asciiz or fixed len?
                stream.write_asciiz_string (value, obj[key + ':offset'])
                #raise RuntimeError (type + " not implemented")
            elif type == 'STRSIZED':
                # FIXME: encoding
                stream.write_dword (len (value) + 1, offset + local_offset)
                stream.write_sized_string (value + '\0', offset + local_offset + 4, len (value) + 1)
            elif type == 'BYTES':
                value = stream.write_blob (value, offset + local_offset)
            elif type.startswith ('_'):
                pass
            else:
                raise ValueError ("Unknown data type: " + type)


    def get_struc_size (self, desc, obj = None):
        total_size = 0
        
        for d in desc:
            key = d['key']
            type = d['type']
            local_offset = d['off']

            
            if type == 'BYTE':
                size = 1
            elif type == 'CTLTYPE':
                size = 1
            elif type == 'WORD':
                size = 2
            elif type == 'DWORD':
                size = 4
            elif type == 'POINT':
                size = 4
            elif type == 'RECT':
                size = 8
            elif type == 'CTLID':
                size = 2
            elif type == 'RGBA':
                size = 4
            elif type == 'STR2':
                size = 2
            elif type == 'STR4':
                size = 4
            elif type == 'STR8':
                size = 8
            elif type == 'STR32':
                size = 32
            elif type == 'RESREF':
                size = 8
            elif type == 'STRREF':
                size = 4
            elif type == 'RESTYPE':
                size = 2
            elif type == 'STROFF':
                #raise RuntimeError (type + " not implemented")
                # NOTE: that is only a size of the pointer, not the string itself
                size = 4
            elif type == 'STRSIZED':
                # FIXME: encoding
                if obj is not None:
                    value = obj[key]
                    size = 4 + len (value)
                else:
                    size = 4 # FIXME: eek!
            elif type == 'BYTES':
                size = d['size']
                #value = obj[key]
                #size = len (value)
            elif type.startswith ('_'):
                # Ignore the fields starting with '_'
                size = 0
            else:
                raise ValueError ("Unknown data type: " + type)

            total_size = max (total_size, local_offset + size)

        return total_size
    

    def print_date_by_desc (self, obj, d):
        p_offset = self.get_option ('format.print_offset')
        p_type = self.get_option ('format.print_type')
        p_size = self.get_option ('format.print_size')
        
        key = d['key']
        rec_type = d['type']
        off = d['off']
        label = d['label']
        
        try: base_offset = obj['_offset']
        except: base_offset = 0

        try: size = d['size']
        except: size = self.get_struc_size ([ {'off': 0, 'type': rec_type, 'key': key , 'size': 0}])

        try: enum = d['enum']
        except: enum = None

        try: mask = d['mask']
        except: mask = None

        try: count = d['count']
        except: count = 1

        for index in range (count):
            if count > 1:
                value = obj[key][index]
            else:
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
            elif enum is not None:
                if type (enum) == types.DictType:
                    try: value2 = '(' + enum[value] + ')'
                    except: pass
    
                elif type (enum) == types.StringType:
                    if not core.ids.has_key (enum):
                        try:
                            # FIXME: ugly & should use 'IDS' instead of 0x3F0
                            ids = ResourceStream ().open (enum, 0x03F0).load_object ()
                            ids.read ()
                            core.ids[enum] = ids
                        except:
                            pass
    
                    try: value2 = '(' + core.ids[enum].ids[value] + ')'
                    except: pass
                        
                    
            elif mask is not None:
                value2 = '(' + string.join (map (lambda m, mask=mask: mask[m], filter (lambda m, v=value: (m & v) == m, mask.keys ())), '|') + ')'

            if p_offset:
                print "0x%04X" %(base_offset + off),
            if p_type:
                print "%-6s" %rec_type,
            if p_size:
                print "%3d" %size,
                
            if count > 1:
                print label + '[%d]:' %index, value, value2
            else:
                print label + ':', value, value2

            off += size


    def get_option (self, key):
        if self.options.has_key (key):
            return self.options[key]
        else:
            return core.get_option (key)


    def set_option (self, key, value):
        self.options[key] = value



# FIXME: should be in chui.py
ctltype_hash = {
    0 : 'button/pixmap',
    2 : 'slider',
    3 : 'textedit',
    5 : 'textarea',
    6 : 'label?',
    7 : 'scrollbar',
    }



def register_format (signature, version, klass,  desc = None):
    core.register_format (signature, version, klass,  desc)


# End of file format.py
