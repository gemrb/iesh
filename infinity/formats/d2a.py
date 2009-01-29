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
import sys
from infinity.format import Format, register_format

class D2A_Format (Format):
    def __init__ (self):
        Format.__init__ (self)
        #self.expect_signature = '2DA'

        self.rows = []
        self.cols = []
        self.cells = {}


    def read (self, stream):
        s = ""
        line_no = 0

        self.signature = stream.get_line ().strip ()
        # FIXME: check the header
        
        self.default_value = stream.get_line ().strip ()
        
        s = stream.get_line ()
        s = s.strip ()
        # FIXME: canonize the column names
        self.cols = map (lambda s: s.strip (), s.split (None))
        line_no = 3
        
        while s is not None:
            s = stream.get_line ()
            if s is None:
                break
            
            line_no = line_no + 1

            s = s.strip ()
            if s == '':
                continue

##            if line_no == 1 and (re.match ("^[0-9]+$", s) or re.match ("^IDS", s)):
##                continue
##            if line_no == 2 and (re.match ("^[0-9]+$", s) or re.match ("^IDS", s)):
##                continue
##            if line_no == 3 and (re.match ("^[0-9]+$", s) or re.match ("^IDS", s)):
##                continue

            values = s.split (None)
            key = values[0]
            values = values[1:]
            key = key.strip ()
            values = map (lambda v: v.strip (), values)
            self.rows.append (key)

            for col in self.cols:
                try: 
                    value = values[0]
                    values.pop (0)
                except: 
                    value = None
                
                self.cells[(key, col)] = value

    def get (self, row, col):
        row = self.get_row_name (row)
        col = self.get_col_name (col)

        if row != '' and col != '':
            return self.cells[(row, col)]
        elif row != '':
            return row
        elif col != '':
            return col
        else:
            return ''


    def get_row_name (self, row):
        # FIXME: canonize
        if row == -1 or row == '':
            return ''
        elif type (row) == type (''):
            if self.rows.index (row) >= 0:
                return row
        else:
            return self.rows[row]


    def get_col_name (self, col):
        # FIXME: canonize
        if col == -1 or col == '':
            return ''
        elif type (col) == type (''):
            if self.cols.index (col) >= 0:
                return col
        else:
            return self.cols[col]


    def get_row (self, row, include_heading = False):
        res = []
        row = self.get_row_name (row)
        
        if include_heading:
            res.append (self.get (row, ''))
            
        for col in self.cols:
            res.append (self.get (row, col))

        return res


    def get_col (self, col, include_heading = False):
        res = []
        col = self.get_col_name (col)
        
        if include_heading:
            res.append (self.get ('', col))
            
        for row in self.rows:
            res.append (self.get (row, col))

        return res


    def trim (self):
        # TODO: replaces values equal to default with implicit default
        pass


    def get_col_width (self, col):
        cols = self.get_col (col, include_heading = True)
        return reduce (lambda m, n: max (m, len (n)), cols, 0)


    # FIXME: options for same column width, minimal width, using tabs, left alignment, ...
    def printme (self):
        print 'Signature:', self.signature
        print 'Default value:', self.default_value
        print self.cols
        for row in self.rows:
            values = self.get_row (row)
            print row + ':', 
            for v in values:
                if v is None:
                    break
                print v,
            print
        
        hsize = self.get_col_width (-1) 
        sizes = map (self.get_col_width, self.get_row (-1))
        
        for row_name in self.get_col (-1, include_heading = True):
            values = self.get_row (row_name, include_heading = False)
            
            print row_name.ljust (hsize),
            for i in range (len (values)):
                value = values[i]
                print value.rjust (sizes[i]),
            print

register_format ('2DA', '', D2A_Format)
