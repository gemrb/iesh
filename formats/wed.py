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

# RCS: $Id: wed.py,v 1.1 2006/07/08 14:29:27 edheldil Exp $

from format import Format, register_format, core

class WED_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'WED'

        self.overlay_list = []

        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'overlay_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of overlays' },

            { 'key': 'door_cnt',
              'type': 'DWORD',
              'off': 0x000C,
              'label': '# of doors' },

            { 'key': 'overlay_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Overlay offset' },

            { 'key': 'secondary_header_off',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Secondary headers offset' },

            { 'key': 'door_off',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Doors offset' },

            { 'key': 'door_tile_cell_indices_off',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Door tile cell indices offset' },

            )

        self.overlay_desc = (
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Width'},

            { 'key': 'height',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Height'},

            { 'key': 'tileset',
              'type': 'RESREF',
              'off': 0x0004,
              'label': 'Tileset'},

            { 'key': 'unknown_0C',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Unknown 0C'},

            { 'key': 'tilemap_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Offset to tilemap'},

            { 'key': 'tile_index_lookup_off',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Offset to tile index lookup'},

            )
        


    def decode_file (self):
        self.decode_header ()

        off = self.header['overlay_off']
        for i in range (self.header['overlay_cnt']):
            obj = {}
            self.decode_overlay (off, obj)
            self.overlay_list.append (obj)
            off = off + 24



    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.overlay_list:
            print 'Overlay #%d' %i
            self.print_overlay (obj)
            i = i + 1
            

    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_overlay (self, offset, obj):
        self.decode_by_desc (offset, self.overlay_desc, obj)
        
    def print_overlay (self, obj):
        self.print_by_desc (obj, self.overlay_desc)

        
register_format ('WED', 'V1.3', WED_Format)
