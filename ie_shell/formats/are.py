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

# RCS: $Id: pro.py,v 1.1 2006/07/08 14:29:26 edheldil Exp $

from ie_shell.formats.format import Format, register_format, core

class ARE_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'AREA'


        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'wed',
              'type': 'RESREF',
              'off': 0x0008,
              'label': 'Corresponding WED file' },

            { 'key': 'unsaved_time',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Seconds since last save' },


            { 'key': 'area_flag',
              'type': 'DWORD',
              'off': 0x0014,
              'mask': {
                  0x01: 'can save',
                  0x02: 'tutorial',
                  0x04: 'dead magic',
                  0x08: 'dream'
                  },
              'label': 'Area flag (AREAFLAG.IDS)'},

            { 'key': 'north_area',
              'type': 'RESREF',
              'off': 0x0018,
              'label': 'Area to the North'},

            { 'key': 'unknown_20',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Unknown north 20'},

            { 'key': 'east_area',
              'type': 'RESREF',
              'off': 0x0024,
              'label': 'Area to the East'},

            { 'key': 'unknown_2C',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown east 20'},

            { 'key': 'south_area',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Area to the South'},

            { 'key': 'unknown_38',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'Unknown south 38'},

            { 'key': 'west_area',
              'type': 'RESREF',
              'off': 0x003C,
              'label': 'Area to the West'},

            { 'key': 'unknown_44',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Unknown west 44'},


            { 'key': 'flags',
              'type': 'WORD',
              'off': 0x0048,
              'mask': {
                  0x01: 'outdoor',
                  0x02: 'day/night',
                  0x04: 'weather',
                  0x08: 'city',
                  0x10: 'forest',
                  0x20: 'dungeon',
                  0x40: 'extended night',
                  0x80: 'can rest inddors',
                  },
              'label': 'Flag (AREATYPE.IDS)'},


            { 'key': 'rain_chance',
              'type': 'WORD',
              'off': 0x004A,
              'label': 'Rain chance'},

            { 'key': 'snow_chance',
              'type': 'WORD',
              'off': 0x004C,
              'label': 'Snow chance'},

            { 'key': 'fog_chance',
              'type': 'WORD',
              'off': 0x004E,
              'label': 'Fog chance (unimpl)'},

            { 'key': 'lightning_chance',
              'type': 'WORD',
              'off': 0x0050,
              'label': 'Lightning chance'},

            { 'key': 'unknown_52',
              'type': 'WORD',
              'off': 0x0052,
              'label': 'Unknown 52'},


            { 'key': 'actor_off',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Actors offset'},

            { 'key': 'actor_cnt',
              'type': 'WORD',
              'off': 0x0058,
              'label': '# of actors'},

            { 'key': 'infopoint_cnt',
              'type': 'WORD',
              'off': 0x005A,
              'label': '# of infopoints, triggerpoints and exits'},

            { 'key': 'infopoint_off',
              'type': 'DWORD',
              'off': 0x005C,
              'label': 'Offset of infopoints, triggerpoints and exits'},

            { 'key': 'spawnpoint_off',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Spawnpoint offset'},

            { 'key': 'spawnpoint_cnt',
              'type': 'DWORD',
              'off': 0x0064,
              'label': '# of spawnpoints'},

            { 'key': 'entrance_off',
              'type': 'DWORD',
              'off': 0x0068,
              'label': 'Entrances offset'},

            { 'key': 'entrance_cnt',
              'type': 'DWORD',
              'off': 0x006C,
              'label': '# of entrances'},

            { 'key': 'container_off',
              'type': 'DWORD',
              'off': 0x0070,
              'label': 'Containers offset'},

            { 'key': 'container_cnt',
              'type': 'WORD',
              'off': 0x0074,
              'label': '# of containers'},

            { 'key': 'item_cnt',
              'type': 'WORD',
              'off': 0x0076,
              'label': '# of items'},

            { 'key': 'item_off',
              'type': 'DWORD',
              'off': 0x0078,
              'label': 'Item offset'},

            { 'key': 'vertex_off',
              'type': 'DWORD',
              'off': 0x007C,
              'label': 'Vertices offset'},

            { 'key': 'vertex_cnt',
              'type': 'WORD',
              'off': 0x0080,
              'label': '# of vertices'},

            { 'key': 'ambient_cnt',
              'type': 'WORD',
              'off': 0x0082,
              'label': '# of ambient sounds'},

            { 'key': 'ambient_off',
              'type': 'DWORD',
              'off': 0x0084,
              'label': 'Ambients offset'},

            )




    def decode_file (self):
        self.decode_header ()
#        if self.header['projectile_type'] == 3:
#            self.decode_area_header ()


    def print_file (self):
        self.print_header ()
#        if self.header['projectile_type'] == 3:
#            self.print_area_header ()


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

#     def decode_area_header (self):
#         self.area_header = {}
#         self.decode_by_desc (0x0000, self.area_header_desc, self.area_header)
        
#     def print_area_header (self):
#         self.print_by_desc (self.area_header, self.area_header_desc)

        
register_format ('AREA', 'V1.0', ARE_Format)
