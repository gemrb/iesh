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

class Cache:
    def __init__ (self):
        self.objects = {}
        self.first = -1
        self.last = 0
        self.max_count = 0
        self.max_size = 0

    def flush (self):
        self.objects = {}

    def get (self, key):
        try:
            rec = self.objects[key]
            self.
            rec[1] = 
        else:
            return None

    def add (self, key, obj):
        self.add_permanent (key, obj)
        self.lru.append (obj)

    def add_permanent (self, key, obj):
        if key in self.objects:
            obj_old = self.objects[key]
            i = self.lru.index (obj_old)
            if i >= 0:
                self.lru.pop (i)
        self.objects[key] = obj

    def trim (self):
        while self.max_count and len (self.lru) > self.max_count:
            key = self.lru.pop (0)
            self.objects.del (key)


# End of file defaults.py
