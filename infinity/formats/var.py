# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2009 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

# Conforms to IESDP 4.5.2008

from infinity import core
from infinity.format import Format, register_format

class VAR_Format (Format):

    header_desc = (
                   )
    variable_desc = (
            { 'key': 'scope',
              'type': 'STR8',
              'off': 0x0000,
              'label': 'Scope' },
            
            { 'key': 'name',
              'type': 'STR32',
              'off':0x0008,
              'label': 'Name'},
            
            { 'key': 'value',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Value' },
            )


    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'None'
        self.variable_list = []


    def read (self, stream):
        size = self.get_struc_size (self.variable_desc)
        off = 0
        while True:
            obj = {}
            try:
                self.read_struc (stream, off, self.variable_desc, obj)
            except:  # FIXME:  specify the actual exception class
                break
            self.variable_list.append (obj)
            off += size
            

    def printme (self):
        for obj in self.variable_list:
            self.print_struc (obj, self.variable_desc)



        
register_format (VAR_Format, signature='902     ', extension='VAR', name='VAR')
