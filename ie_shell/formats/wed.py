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

from ie_shell.formats.format import Format, register_format, core

class WED_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'WED'

        self.secondary_header = {}
        self.overlay_list = []
        self.door_list = []

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
        
        self.secondary_header_desc = (
            { 'key': 'polygon_cnt',
              'type': 'DWORD',
              'off': 0x0000,
              'label': '# of polygons'},

            { 'key': 'polygon_off',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Polygons offset'},

            { 'key': 'vertex_off',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Vertices offset'},

            { 'key': 'wallgrp_off',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Wall groups offset'},

            { 'key': 'polygon_lut_off',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Polygon indices LUT offset'},

            )

        self.door_desc = (
            { 'key': 'door_name',
              'type': 'STR8',
              'off': 0x0000,
              'label': 'Door name'},

            { 'key': 'unknown_08',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'Unknown 08'},

            { 'key': 'door_tile_cell_ndx',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'First door tile cell index'},

            { 'key': 'door_tile_cell_cnt',
              'type': 'WORD',
              'off': 0x000C,
              'label': 'Door tile cell count'},

            { 'key': 'open_door_poly_cnt',
              'type': 'WORD',
              'off': 0x000E,
              'label': '# of open door polygons'},

            { 'key': 'closed_door_poly_cnt',
              'type': 'WORD',
              'off': 0x0010,
              'label': '# of closed door polygons'},

            { 'key': 'open_door_poly_off',
              'type': 'DWORD',
              'off': 0x0012,
              'label': 'Offset of open door polygons'},

            { 'key': 'closed_door_poly_off',
              'type': 'DWORD',
              'off': 0x0016,
              'label': 'Offset of closed door polygons'},

            )

        self.tilemap_desc = (
            { 'key': 'tile_index_lut_ndx',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Primary tile index LUT start index'},

            { 'key': 'tile_index_lut_cnt',
              'type': 'WORD',
              'off': 0x0002,
              'label': '# of tiles in primary tile index LUT'},

            { 'key': 'secondary_tis_index',
              'type': 'WORD',
              'off': 0x0004,
              'label': 'Index from TIS (secondary)'},

            { 'key': 'overlay_mask',
              'type': 'BYTE',
              'off': 0x0006,
              'label': 'Mask of drawn overlays'},

            { 'key': 'unknown_07',
              'type': 'BYTES',
              'off': 0x0007,
              'size': 3,
              'label': 'Unknown 07'},

            )

        # Door tile cells desc

        # Tile index lookup table desc

        self.wallgroup_desc = (
            { 'key': 'polygon_ndx',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Start polygon index'},

            { 'key': 'polygon_cnt',
              'type': 'WORD',
              'off': 0x0002,
              'label': '# of Polygon'},

            )

        self.polygon_desc = (
            { 'key': 'vertex_ndx',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Start vertex index'},

            { 'key': 'vertex_cnt',
              'type': 'DWORD',
              'off': 0x0004,
              'label': '# of vertices'},

            { 'key': 'flags',
              'type': 'BYTE',
              'off': 0x0008,
              'mask': {
                  0x01: 'shade wall',
                  0x02: 'hovering',
                  0x04: 'cover anims',
                  0x08: 'cover anims 2',
                  0x10: 'unknown 4',
                  0x20: 'unknown 5',
                  0x40: 'unknown 6',
                  0x80: 'door?',
                  },
              'label': 'Passability flags'},

            { 'key': 'unknown_09',
              'type': 'BYTE',
              'off': 0x0009,
              'label': 'Unknown 09'},

            { 'key': 'bbox_x1',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Bounding box X min'},

            { 'key': 'bbox_x2',
              'type': 'WORD',
              'off': 0x000C,
              'label': 'Bounding box X max'},

            { 'key': 'bbox_y1',
              'type': 'WORD',
              'off': 0x000E,
              'label': 'Bounding box Y min'},

            { 'key': 'bbox_y2',
              'type': 'WORD',
              'off': 0x0010,
              'label': 'Bounding box Y max'},
            
            )

        # Polygon index LUT desc

        self.vertex_desc = (
            { 'key': 'x',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'X'},

            { 'key': 'y',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Y'},
            
            )

    def decode_file (self):
        self.decode_header ()
        self.decode_secondary_header (self.header['secondary_header_off'], self.secondary_header)

        off = self.header['overlay_off']
        for i in range (self.header['overlay_cnt']):
            obj = {}
            self.decode_overlay (off, obj)
            self.overlay_list.append (obj)
            off = off + 24

        off = self.header['door_off']
        for i in range (self.header['door_cnt']):
            obj = {}
            self.decode_door (off, obj)
            self.door_list.append (obj)
            off = off + 26



    def print_file (self):
        self.print_header ()
        self.print_secondary_header ()

        i = 0
        for obj in self.overlay_list:
            print 'Overlay #%d' %i
            self.print_overlay (obj)
            i = i + 1
            
        i = 0
        for obj in self.door_list:
            print 'Door #%d' %i
            self.print_door (obj)
            i = i + 1
            

    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)

        
    def decode_secondary_header (self, offset, obj):
        self.decode_by_desc (offset, self.secondary_header_desc, obj)
        
    def print_secondary_header (self):
        self.print_by_desc (self.secondary_header, self.secondary_header_desc)
        

    def decode_overlay (self, offset, obj):
        self.decode_by_desc (offset, self.overlay_desc, obj)
        
    def print_overlay (self, obj):
        self.print_by_desc (obj, self.overlay_desc)

        
    def decode_door (self, offset, obj):
        self.decode_by_desc (offset, self.door_desc, obj)

        obj['open_door_poly_list'] = []
        off = obj['open_door_poly_off']
        for i in range (obj['open_door_poly_cnt']):
            obj2 = {}
            self.decode_polygon (off, obj2)
            obj['open_door_poly_list'].append (obj2)
            off = off + 34

        obj['closed_door_poly_list'] = []
        off = obj['closed_door_poly_off']
        for i in range (obj['closed_door_poly_cnt']):
            obj2 = {}
            self.decode_polygon (off, obj2)
            obj['closed_door_poly_list'].append (obj2)
            off = off + 34

        
    def print_door (self, obj):
        self.print_by_desc (obj, self.door_desc)

        i = 0
        for obj2 in obj['open_door_poly_list']:
            print 'Open Poly #%d' %i
            self.print_polygon (obj2)
            i = i + 1

        i = 0
        for obj2 in obj['closed_door_poly_list']:
            print 'Closed Poly #%d' %i
            self.print_polygon (obj2)
            i = i + 1

        
    def decode_tilemap (self, offset, obj):
        self.decode_by_desc (offset, self.tilemap_desc, obj)
        
    def print_tilemap (self, obj):
        self.print_by_desc (obj, self.tilemap_desc)

        
    def decode_wallgroup (self, offset, obj):
        self.decode_by_desc (offset, self.wallgroup_desc, obj)
        
    def print_wallgroup (self, obj):
        self.print_by_desc (obj, self.wallgroup_desc)


    def decode_polygon (self, offset, obj):
        self.decode_by_desc (offset, self.polygon_desc, obj)
        
    def print_polygon (self, obj):
        self.print_by_desc (obj, self.polygon_desc)

        
    def decode_vertex (self, offset, obj):
        self.decode_by_desc (offset, self.vertex_desc, obj)
        
    def print_vertex (self, obj):
        self.print_by_desc (obj, self.vertex_desc)

        
        

register_format ('WED', 'V1.3', WED_Format)
