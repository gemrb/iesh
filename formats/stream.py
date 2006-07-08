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

# RCS: $Id: stream.py,v 1.3 2006/07/08 14:29:27 edheldil Exp $

import gzip
import os.path
import re
import string
import struct

from plugins import core

class Stream:
    def __init__ (self):
        self.is_open = False
        
    def open (self):
        pass
    
    def close (self):
        pass
    
    def seek (self, offset):
        pass

    def read (self, count = None):
        pass

    def readline (self):
        pass


    def get_char (self, offset):
        # offset == None means "current offset" here
        if offset != None:
            self.seek (offset)
            
        return self.read (1)
        #v = self.read (1)
        #return struct.unpack ('c', v)[0]

    def get_line (self):
        #return self.readline ()
        return self.decode_line_string ()

    def decode_word (self, offset):
        # offset == None means "current offset" here
        if offset != None:
            self.seek (offset)
        v = self.read (2)
        return struct.unpack ('H', v)[0]

    def decode_dword (self, offset):
        # offset == None means "current offset" here
        if offset != None:
            self.seek (offset)
        v = self.read (4)
        return struct.unpack ('I', v)[0]

    def decode_sized_string (self, offset, size):
        # offset == None means "current offset" here
        if offset != None:
            self.seek (offset)
        v = self.read (size)
        
        return struct.unpack ('%ds' %size, v)[0]

    def decode_asciiz_string (self, off):
        s = ''
        
        while 1:
            c = self.get_char (off)
            if c == '\0': break
            s = s + c
            off = off + 1
            
        return s

    def decode_line_string (self):
        s = ''
        
        while 1:
            c = self.get_char (None)
            if c == '\n': break
            if c == '':
                if s == '':
                    s = None
                break
            
            s = s + c
            
        return s

    def decode_resref (self, off):
        return self.decode_sized_string (off, 8)

    def decode_blob (self, offset, size = None):
        # offset == None means "current offset" here
        # size == None means "till the end of stream"
        if offset != None:
            self.seek (offset)

        return self.read (size)
        

    def get_signature (self):
        was_open = self.is_open
        if not self.is_open:
            self.open ()

        s = self.decode_sized_string (0, 8)

        if not was_open:
            self.close ()
        else:
            self.seek (0)


        if re.match ("[0-9]{1,4}[\r\n ]", s) or re.match ("0[xX][0-9A-Fa-f]{1,4} ", s) or re.match ("-1[\r\n]", s):
            signature = "IDS"
            version = ""
        else:
            signature = s[0:4].strip ()
            version = s[4:8].strip ()

        return (signature, version)

    def get_format (self, type = 0):
        signature, version = self.get_signature ()
        fmt = core.get_format (signature, version)
        
        if fmt == None and type != 0:
            fmt = core.get_format_by_type (type)

        return fmt


    def load_object (self, type = 0):
        fmt = self.get_format ()
        return fmt (self)



class FileStream (Stream):
    def __init__ (self, filename):
        Stream.__init__ (self)

        self.filename = filename

    def open (self):
        self.fh = open (self.filename, "r")
        self.is_open = True

    def close (self):
        self.fh.close ()
        self.is_open = False

    def seek (self, offset):
        self.fh.seek (offset)

    def read (self, size = None):
        if size != None:
            return self.fh.read (size)
        else:
            return self.fh.read ()
        

    def __repr__ (self):
        return "<FileStream: %s>" %self.filename


class MemoryStream (Stream):
    def __init__ (self, membuffer):
        Stream.__init__ (self)

        self.buffer = membuffer

    def open (self):
        self.offset = 0
        self.is_open = True

    def decrypt (self):
        for i in range (len (self.buffer)):
            print chr (ord (self.buffer[i]) ^ ord (core.xor_key[i]))

    def close (self):
        self.is_open = False
    
    def seek (self, offset):
        self.offset = offset

    def read (self, count = None):
        if count != None:
            data = self.buffer[self.offset:self.offset+count]
        else:
            data = self.buffer[self.offset:]
            
        self.offset = self.offset + len (data)
        return data



class ResourceStream (MemoryStream):
    def __init__ (self, name, type = None):
        MemoryStream.__init__ (self, '')
        self.resref = name
        self.type = type

    def open (self):
        if core.keys == None:
            raise RuntimeError, "Core game files are not loaded. See load_game ()."

        oo = core.keys.get_resref_by_name_re (self.resref)
        if self.type != None:
            oo = filter (lambda o: o['type'] == self.type, oo)

        if len (oo) > 1 and self.type == None:
            raise RuntimeError, "More than one result"

        o = oo[0]
     
        src_file = core.keys.bif_list[o['locator_src_ndx']]
        b = core.formats['BIFF'] (os.path.join (core.game_dir, src_file['file_name']))
        b.decode_file ()
        obj = b.file_list[o['locator_ntset_ndx']]
        b.get_file_data (obj)

        self.buffer = obj['data']
        MemoryStream.open (self)

    def load_object (self):
        return Stream.load_object (self, self.type)


    def __repr__ (self):
        return "<ResStream: %s>" %self.resref


class CompressedStream (MemoryStream):
    def __init__ (self, membuffer):
        MemoryStream.__init__ (self, gzip.zlib.decompress (membuffer))
