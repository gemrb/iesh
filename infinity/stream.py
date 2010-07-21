# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2010 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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
Implement *Stream, classes for reading  IE files.

Implement *Stream classes for reading IE data primitives
from normal files, memory buffers and from files in IE specific 
`filesystem' addressed by RESREFs.

Classes:
  Stream - base class implementing reading of IE primitives
  FileStream - read from files contained in filesystem
  MemoryStream - read from memory buffers (strings)
  ResourceStream - read IE object referenced by RESREF
  CompressedStream - read compressed buffer
"""


import gzip
import os.path
import re
import string
import struct

from infinity import core


class Stream (object):
    """
    Base abstract class for reading and writing IE files. 
    
    It implements the basic open / read / write / seek / close
    API to be implemented in the subclasses, as well as
    functions for reading primitive IE data types like RESREF or WORD.
    """
    
    def __init__ (self):
        self.is_open = False
        self.options = {}


    def __del__ (self):
        """Destructor"""
        # FIXME: possibly close() only when autoclose flag is set
        self.close ()


    def open (self, name,  mode = 'r'):
        # do the real open here
        self.is_open = True
        self.name = name
        self.coverage = []
        return self


    def close (self):
        if not self.is_open:
            return
            
        if self.get_option ('stream.debug_coverage'):
            self.print_coverage ()
        self.is_open = False


    def seek (self, offset):
        """Set position for next read (current offset) to `offset'.
        Override in subclasses."""
        pass

    def read (self, count = None):
        """Read `count' of bytes at the current offset and update the offset.
        Override in subclasses."""
        pass

    def write (self, data, count = None):
        """Write `data' to current offset in file.
       Override in subclasses."""
        pass

    # Methods for reading and writing primitive IE data types

    def get_char (self, offset = None):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
            
        return self.read (1)
        #v = self.read (1)
        #return struct.unpack ('c', v)[0]

    def put_char (self, char, offset = None):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
            
        self.write (char, 1)
        
    def get_line (self):
        #return self.readline ()
        return self.read_line_string ()

    def put_line (self):
        #FIXME
        pass

    def read_word (self, offset):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        v = self.read (2)
        return struct.unpack ('<H', v)[0]

    def write_word (self, value, offset = None):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        bytes = struct.pack ('<H', value)
        self.write (bytes)

    def read_dword (self, offset):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        v = self.read (4)
        return struct.unpack ('<I', v)[0]

    def write_dword (self, value, offset = None):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        bytes = struct.pack ('<I', value)
        self.write (bytes)

    def read_sized_string (self, offset, size):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        v = self.read (size)
        # FIXME: remove the trailing zeros
        
        return struct.unpack ('%ds' %size, v)[0]

    def write_sized_string (self, value, offset, size):
        # offset == None means "current offset" here
        if offset is not None:
            self.seek (offset)
        
        # FIXME: pad with zeros
        bytes = struct.pack ('%ds' %size, value)
        self.write (bytes)

    def read_asciiz_string (self, off):
        s = ''
        
        while 1:
            c = self.get_char (off)
            if c == '\0': break
            s = s + c
            off = off + 1
            
        return s

    def read_line_string (self):
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

    # FIXME: (read|write)_resref should not be here
    def read_resref (self, off):
        return self.read_sized_string (off, 8)

    def write_resref (self, value, off):
        self.write_sized_string (value, off, 8)

    def read_blob (self, offset, size = None):
        # offset == None means "current offset" here
        # size == None means "till the end of stream"
        if offset is not None:
            self.seek (offset)

        return self.read (size)
        
    def write_blob (self, value, offset, size = None):
        # offset == None means "current offset" here
        # size == None means "till the end of stream"
        if offset is not None:
            self.seek (offset)

        return self.write (value)
        

    # Helper methods

    def get_signature (self):
        was_open = self.is_open
        #if not self.is_open:
        #    self.open ()

        s = self.read_sized_string (0x0000, 8)

        #if not was_open:
        #    self.close ()
        #else:
        #    self.seek (0)


        if s == '902     ':
            signature = "VAR"
            version = ""
        elif re.match (" ?2DA[\r\n\t ]", s):
            signature = "2DA"
            version = ""
        elif re.match ("[0-9]{1,4}[\r\n ]", s) or re.match ("0[xX][0-9A-Fa-f]{1,4} ", s) or re.match ("-1[\r\n]", s):
            signature = "IDS"
            version = ""
        elif s == "SC\nCR\nCO" or s == "SC\r\nCR\r\n":
            signature = "BCS"
            version = ""
        elif s.startswith ("IF\n") or s.startswith ("IF\r\n"):
            signature = "BAF"
            version = ""
        else:
            signature = s[0:4].strip ()
            version = s[4:8].strip ()

        return (signature, version)

    def get_format (self, type = 0):
        signature, version = self.get_signature ()
        fmt = core.get_format (signature, version)
        
        if fmt is None and type != 0:
            fmt = core.get_format_by_type (type)

        if fmt is None:
            raise RuntimeError, "Unknown format: %s %s"%(signature, version)

        return fmt


    def load_object (self, type = 0):
        #print self
        fmt = self.get_format ()
        obj = fmt ()
        self.seek (0)
        obj.read (self)
        return obj


    def coverage_add (self, offset, size, some_info_tbd):
        d = offset +size - len (self.coverage)
        if d > 0:
            self.coverage.extend ([0] * d)
        for i in range (offset,  offset + size):
            self.coverage[i] += 1


    def print_coverage (self):
        def print_single (offset,  value):
            print "  0x%04x: %d" %(offset,  value)

        def print_range (offset1,  offset2,  value):
            if offset2 == offset1:
                print_single (offset1,  value)
            else:
                print "  0x%04x - 0x%04x: %d" %(offset1,  offset2,  value)

        print "Coverage (%s):" %self.name
        from_offset = None
        
        for i in range (len (self.coverage)):
            if self.coverage[i] == 0 and from_offset is None:
                from_offset = i
            elif self.coverage[i] == 0:
                pass
            elif self.coverage[i] > 1:
                if from_offset is not None:
                    print_range (from_offset,  i - 1,  0)
                    from_offset = None
                print_single (i,  self.coverage[i])
            else:
                if from_offset is not None:
                    print_range (from_offset,  i - 1,  0)
                    from_offset = None
                    
        if from_offset is not None:
            print_range (from_offset,  i - 1,  0)
            from_offset = None


    def get_option (self, key):
        if self.options.has_key (key):
            return self.options[key]
        else:
            return core.get_option (key)


    def set_option (self, key, value):
        self.options[key] = value




class FileStream (Stream):
    """Specialized Stream for working with normal files in filesystem"""

    def __init__ (self):
        Stream.__init__ (self)

    def open (self, filename, mode = 'r'):
        # FIXME: reset offset?
        Stream.open (self, filename,  mode)
        self.is_open = False
        self.filename = filename
        self.fh = open (self.filename, mode)
        self.is_open = True
        
        if self.get_option ('stream.debug_coverage'):
            size = os.stat (filename)[6]
            self.coverage = [0] * size
            
        return self

    def close (self):
        if not self.is_open:
            return
            
        self.fh.close ()
        Stream.close (self)

    def seek (self, offset):
        self.fh.seek (offset)

    def read (self, size = None):
        # FIXME: do some caching/buffering here?

        #if size == None:
        #   raise RuntimeError ()

        if self.get_option ('stream.debug_coverage'):
            off = self.fh.tell ()

        #if size != None:
        value = self.fh.read (size)
        #else:
        #   value = self.fh.read ()

        if self.get_option ('stream.debug_coverage'):
            #sz = len (value)
            self.coverage_add (off,  size,  None)
        return value


    def write (self, bytes, size = None):
        #if size != None:
        #    self.fh.write (bytes, size)
        #else:
        self.fh.write (bytes)

    def __repr__ (self):
        return "<FileStream: %s at 0x%08x>" %(self.filename, id (self))


class MemoryStream (Stream):
    """Stream for working with memory buffers instead of files."""
    def __init__ (self):
        Stream.__init__ (self)

    def open (self, membuffer,  name = '?'):
        Stream.open (self, name,  '')
        self.buffer = membuffer
        self.offset = 0
        return self

    def decrypt (self):
        for i in range (len (self.buffer)):
            print chr (ord (self.buffer[i]) ^ ord (core.xor_key[i]))

    def seek (self, offset):
        self.offset = offset

    def read (self, count = None):
        if count is not None:
            data = self.buffer[self.offset:self.offset+count]
        else:
            data = self.buffer[self.offset:]
            
        self.offset = self.offset + len (data)
        return data

    def __repr__ (self):
        return "<MemoryStream: %s at 0x%08x>" %(self.name, id (self))

class ResourceStream (MemoryStream):
    """Stream for reading RESREFs (files in the IE data `filesystem').
    It requires that the KEY file is loaded in core.keys."""

    def __init__ (self):
        MemoryStream.__init__ (self)

    def open (self, name, type = None,  index = 0):
        self.resref = name
        self.type = type

        if core.keys is None:
            raise RuntimeError, "Core game files are not loaded. See load_game ()."

        oo = core.keys.get_resref_by_name (self.resref)
        if self.type is not None:
            oo = filter (lambda o: o['type'] == self.type, oo)

        if len (oo) > 1 and self.type is None:
            raise RuntimeError, "More than one result"

        o = oo[index]

        # First look for the object in cache and override directories.
        # We have to attach filename extension to the name based on its type when searching
        exts = core.type_to_ext (o['type'])
        for ext in exts:
            obj_file = core.find_file (name + ext)
            if obj_file is not None:
                return FileStream ().open (obj_file)

        # The object was not found in the filesystem, so look for it in BIF archives.
        # Lookup the BIF archive file containing the object
        src_file = core.keys.bif_list[o['locator_src_ndx']]
        bif_file = core.find_file (src_file['file_name'])
        
        bif_stream = FileStream ().open (bif_file)
        b = core.get_format ('BIFF') ()
        b.read (bif_stream)
        obj = b.file_list[o['locator_ntset_ndx']]
        b.get_file_data (bif_stream, obj)

        buffer = obj['data']
        return MemoryStream.open (self, buffer,  name = name)
        
    def load_object (self):
        return Stream.load_object (self, self.type)


    def __repr__ (self):
        return "<ResourceStream: %s at 0x%08x>" %(self.resref, id (self))


class CompressedStream (MemoryStream):
    """Stream for reading compressed files in memory."""
    
    def open (self, membuffer,  name = '?'):
        return MemoryStream.open (self, gzip.zlib.decompress (membuffer),  name)

    def __repr__ (self):
        return "<CompressedStream: %s at 0x%08x>" %(self.name, id (self))
        
# End of file stream.py

