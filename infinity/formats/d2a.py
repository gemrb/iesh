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

from __future__ import print_function

import re
import sys
from infinity.format import Format, register_format

num_re = re.compile ('^[0-9]*$')


class D2A_Format (Format):
    def __init__ (self):
        Format.__init__ (self)
        #self.expect_signature = '2DA'

        self.rows = []
        self.cols = []
        self.rows_hash = {}
        self.cols_hash = {}
        self.cells = []


    def read (self, stream):
        s = ""
        line_no = 0

        self.signature = stream.get_line ().strip ()
        # FIXME: check the header

        self.default_value = stream.get_line ().strip ()

        s = stream.get_line ()
        s = s.strip ()
        # FIXME: canonize the column names
        self.cols = s.split (None)
        self.cols_hash = dict ([ (i, n.upper ()) for i, n in enumerate (self.cols) ])

        line_no = 3

        while s is not None:
            s = stream.get_line ()
            if s is None:
                break

            line_no = line_no + 1

            s = s.strip ()
            if s == '':
                continue

            values = s.split (None)
            key = values.pop (0)
            self.rows.append (key)
            self.rows_hash[key.upper ()] = len (self.rows)

            if len (values) < len (self.cols):
                values.extend ([''] * (len (self.cols) - len (values)))
            self.cells.append (values)


    def get (self, row, col, fill_blanks=True):
        row = self.get_row_id (row)
        col = self.get_col_id (col)

        if row >= 0 and col >= 0:
            if self.cells[row][col] != '' or not fill_blanks:
                return self.cells[row][col]
            else:
                return self.default_value
        elif row != -1:
            return self.rows[row]
        elif col != -1:
            return self.cols[col]
        else:
            return ''


#    def get_row_name (self, row):
#        # FIXME: canonize
#        if row == -1 or row == '':
#            return ''
#        elif type (row) == type (''):
#            if self.rows.index (row) >= 0:
#                return row
#        else:
#            return self.rows[row]
#
#
#    def get_col_name (self, col):
#        # FIXME: canonize
#        if col == -1 or col == '':
#            return ''
#        elif type (col) == type (''):
#            if self.cols.index (col) >= 0:
#                return col
#        else:
#            return self.cols[col]

    def get_row_id (self, name):
        if name == '':
            return -1
        if type (name) == type (''):
            return self.rows_hash[name.upper ()]
        else:
            return name

    def get_col_id (self, name):
        if name == '':
            return -1
        if type (name) == type (''):
            return self.cols_hash[upper (name)]
        else:
            return name

    def get_row (self, row, include_heading = False):
        start = (0, -1)[include_heading == True]
        return [ self.get (row, i, False)  for i in range (start, len (self.cells[self.get_row_id (row)])) ]

#        res = []
#        row = self.get_row_id (row)
#
#        if include_heading:
#            res.append (self.get (row, ''))
#
#        for col in self.cols:
#            res.append (self.get (row, col))
#
#        return res


    def get_col (self, col, include_heading = False):
        start = (0, -1)[include_heading == True]
        return [ self.get (i, col, False)  for i in range (start, len (self.cells)) ]

#        res = []
#        col = self.get_col_id (col)
#
#        if include_heading:
#            res.append (self.get ('', col))
#
#        for row in self.rows:
#            res.append (self.get (row, col))
#
#        return res


    def trim (self):
        # TODO: replaces values equal to default with implicit default
        pass


    def get_col_width (self, col):
        cells = self.get_col (col, True)
        return reduce (lambda m, n: max (m, len (n)), cells, 0)

    def get_col_justification (self, col):
        cells = self.get_col (col, False)
        return reduce (lambda m, n: max (m, num_re.match (n) is not None), cells, False)


    # FIXME: options for same column width, minimal width, using tabs, left alignment, ...
    def printme (self):
        print ('Signature:', self.signature)
        print ('Default value:', self.default_value)
        sizes = map (self.get_col_width, range (-1, len (self.cols)))
        rjusts = map (self.get_col_justification, range (-1, len (self.cols)))
        #print self.cols
        for row in range (-1, len (self.rows)):
            values = self.get_row (row, True)
            for val, size, rjust in zip (values, sizes, rjusts):
                if rjust:
                    print(val.rjust (size), end=' ')
                else:
                    print(val.ljust (size), end=' ')
                #print "%*s" %(size, val),

            print()


register_format (D2A_Format, regexp=" ?2DA[\r\n\t ]", extension='2DA', name='2DA', type=0x3f4)
