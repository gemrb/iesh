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


from __future__ import print_function

import re
import sys

from infinity.format import Format, register_format


class MUS_Format (Format):
    def __init__ (self):
        Format.__init__ (self)
        #self.expect_signature = 'IDS'

        self.name = None
        self.num_entries = 0
        self.playlist = []


    def read (self, stream):
        s = ""
        line_no = 0

        while s is not None:
            s = stream.get_line ()
            if s is None:
                break

            line_no = line_no + 1

            s = s.strip ()
            if s == '':
                continue

            if line_no == 1 and re.match ("^[A-Za-z0-9_-]+$", s.rstrip()):
                self.name = s.rstrip()
                continue
            elif line_no == 2 and re.match ("^[0-9]+$", s.rstrip()):
                self.num_entries = int(s.rstrip())
                continue
            elif line_no >= 3 and line_no <= self.num_entries + 2:
                words = re.split("[ \t]+", s)
                #print (words)
                words.extend([None, None, None, None])
                label = words.pop(0)
                if words[0] and not words[0].startswith('@'):
                    tag = words.pop(0)
                    if words[0] and words[0].startswith('@'):
                        loop = tag
                    else:
                        loop = words.pop(0)
                else:
                    tag = None
                    loop = None
                
                tag2 = words.pop(0)
                end = words.pop(0)

                self.playlist.append((label, tag, loop, tag2, end))
                continue
            elif line_no > self.num_entries + 2:
                break
            else:
                RuntimeError()

 

    def write (self, stream):
        stream.put_line (self.name)
        stream.put_line (str(self.num_entries))

        for pl in self.playlist:
            #print (pl)
            pl = [ (p, '')[p is None]  for p in pl ]
            stream.put_line ("%-9s %-9s %s" %(pl[0], pl[1]+' '+pl[2], pl[3]+' '+pl[4]))


    def printme (self):
        print ('Name:', self.name)
        print ('Num entries:', self.num_entries)

        for pl in self.playlist:
            #print (pl)
            pl = [ (p, '')[p is None]  for p in pl ]
            print ("%-9s %-9s %s" %(pl[0], pl[1]+' '+pl[2], pl[3]+' '+pl[4]))



register_format (MUS_Format, regexp="[A-Za-z][A-Za-z0-9_-]+[\r\n]+[0-9]+[\r\n]+.*", extension='MUS', name='MUS')
