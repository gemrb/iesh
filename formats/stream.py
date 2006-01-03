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

# RCS: $Id: stream.py,v 1.1 2006/01/03 21:18:05 edheldil Exp $

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

    def read (self, count):
        pass



    def get_char (self, offset):
        self.seek (offset)
        return self.read (1)
        #v = self.read (1)
        #return struct.unpack ('c', v)[0]

    def decode_word (self, offset):
        self.seek (offset)
        v = self.read (2)
        return struct.unpack ('H', v)[0]

    def decode_dword (self, offset):
        self.seek (offset)
        v = self.read (4)
        return struct.unpack ('I', v)[0]

    def decode_sized_string (self, offset, size):
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

    def decode_resref (self, off):
        return self.decode_sized_string (off, 8)

    def decode_blob (self, offset, size):
        self.seek (offset)
        return self.read (size)


    def get_format_signature (self):
        was_open = self.is_open
        if not self.is_open:
            self.open ()

        signature = self.decode_sized_string (0, 4).strip ()
        version = self.decode_sized_string (4, 4).strip ()

        if not was_open:
            self.close ()
        else:
            self.seek (0)

        return (signature, version)

    def get_format (self):
        signature, version = self.get_format_signature ()
        return core.get_format (signature, version)


    def load_object (self):
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

    def read (self, size):
        return self.fh.read (size)
        


class MemoryStream (Stream):
    def __init__ (self, membuffer):
        Stream.__init__ (self)

        self.buffer = membuffer

    def open (self):
        self.offset = 0
        self.is_open = True

    def close (self):
        self.is_open = False
    
    def seek (self, offset):
        self.offset = offset

    def read (self, count):
        data = self.buffer[self.offset:self.offset+count]
        self.offset = self.offset + count
        return data



class ResourceStream (MemoryStream):
    def __init__ (self, name, type = 0):
        MemoryStream.__init__ (self, '')
        self.resref = name
        self.type = type

    def open (self):
        if core.keys == None:
            raise RuntimeError, "Core game files are not loaded. See load_game ()."

        oo = core.keys.get_resref_by_name_re (self.resref)
        if self.type != 0:
            oo = filter (lambda o: o['type'] == self.type, oo)

        if len (oo) > 1 and self.type == 0:
            raise RuntimeError, "More than one result"

        o = oo[0]
     
        src_file = core.keys.bif_list[o['locator_src_ndx']]
        b = core.formats['BIFF'] (os.path.join (core.game_dir, src_file['file_name']))
        b.decode_file ()
        obj = b.file_list[o['locator_ntset_ndx']]
        b.get_file_res_data (obj)

        self.buffer = obj['data']
        MemoryStream.open (self)
