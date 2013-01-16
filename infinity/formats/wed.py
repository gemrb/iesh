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


from infinity import core
from infinity.format import Format, register_format

class WED_Format (Format):
    header_desc = (
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

    overlay_desc = (
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
        
    secondary_header_desc = (
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

    door_desc = (
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

    tilemap_desc = (
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

    wallgroup_desc = (
            { 'key': 'polygon_ndx',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Start polygon index'},

            { 'key': 'polygon_cnt',
              'type': 'WORD',
              'off': 0x0002,
              'label': '# of Polygon'},

            )

    polygon_desc = (
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

    vertex_desc = (
            { 'key': 'x',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'X'},

            { 'key': 'y',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Y'},
            
            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'WED'

        self.secondary_header = {}
        self.overlay_list = []
        self.door_list = []
        self.polygon_list = []


    def read (self, stream):
        self.read_header (stream)
        self.read_secondary_header (stream, self.header['secondary_header_off'], self.secondary_header)


        off = self.header['overlay_off']
        for i in range (self.header['overlay_cnt']):
            obj = {}
            self.read_overlay (stream, off, obj)
            self.overlay_list.append (obj)
            off = off + 24

        # NOTE: door is nested, so we can't use read_list () here
        off = self.header['door_off']
        for i in range (self.header['door_cnt']):
            obj = {}
            self.read_door (stream, off, obj)
            self.door_list.append (obj)
            off = off + 26



    def printme (self):
        self.print_header ()
        self.print_secondary_header ()

        i = 0
        for obj in self.overlay_list:
            print('Overlay #%d' %i)
            self.print_overlay (obj)
            i = i + 1

        i = 0
        for obj in self.door_list:
            print('Door #%d' %i)
            self.print_door (obj)
            i = i + 1


    def read_secondary_header (self, stream, offset, obj):
        self.read_struc (stream, offset, self.secondary_header_desc, obj)
        
        self.read_list (stream, 'polygon',  self.secondary_header,)
        # vertices
        # wallgroups
        # polygon indices LUT

    def print_secondary_header (self):
        self.print_struc (self.secondary_header, self.secondary_header_desc)
        self.print_list ('polygon')
        # vertices
        # wallgroups
        # polygon indices LUT

        
    def read_overlay (self, stream, offset, obj):
        self.read_struc (stream, offset, self.overlay_desc, obj)
        obj['tilemap_list'] = []
        cnt = obj['width'] * obj['height']
        size = self.get_struc_size (self.tilemap_desc)

        off2 = obj['tilemap_off']
        tile_index_cnt = 0
        
        for i in range (cnt):
            obj2 = {}
            self.read_tilemap (stream, off2, obj2,  obj)
            obj['tilemap_list'].append (obj2)
            off2 = off2 + size
            tile_index_cnt +=  obj2['tile_index_lut_cnt']

        obj['tile_index_list'] = []
        size = 2 # FIXME: don't hardwire the size
        off2 = obj['tile_index_lookup_off']
        
        for i in range (tile_index_cnt):
            tile_index = stream.read_word (off2)
            obj['tile_index_list'].append (tile_index)
            off2 += size


    def print_overlay (self, obj):
        self.print_struc (obj, self.overlay_desc)

        i = 0
        for obj2 in obj['tilemap_list']:
            print('Tilemap #%d' %i)
            self.print_tilemap (obj2)
            i = i + 1

        print("Tile indices:",  obj['tile_index_list'])
        print()


    def read_door (self, stream, offset, obj):
        self.read_struc (stream, offset, self.door_desc, obj)

        obj['open_door_poly_list'] = []
        off = obj['open_door_poly_off']
        for i in range (obj['open_door_poly_cnt']):
            obj2 = {}
            self.read_polygon (stream, off, obj2)
            obj['open_door_poly_list'].append (obj2)
            off = off + 34

        obj['closed_door_poly_list'] = []
        off = obj['closed_door_poly_off']
        for i in range (obj['closed_door_poly_cnt']):
            obj2 = {}
            self.read_polygon (stream, off, obj2)
            obj['closed_door_poly_list'].append (obj2)
            off = off + 34

        
    def print_door (self, obj):
        self.print_struc (obj, self.door_desc)

        i = 0
        for obj2 in obj['open_door_poly_list']:
            print('Open Poly #%d' %i)
            self.print_polygon (obj2)
            i = i + 1

        i = 0
        for obj2 in obj['closed_door_poly_list']:
            print('Closed Poly #%d' %i)
            self.print_polygon (obj2)
            i = i + 1

        
    def read_tilemap (self, stream, offset, obj, overlay):
        self.read_struc (stream, offset, self.tilemap_desc, obj)
        
    def print_tilemap (self, obj):
        self.print_struc (obj, self.tilemap_desc)
        
    def read_wallgroup (self, stream, offset, obj):
        self.read_struc (stream, offset, self.wallgroup_desc, obj)
        
    def print_wallgroup (self, obj):
        self.print_struc (obj, self.wallgroup_desc)


    def read_polygon (self, stream, offset, obj):
        self.read_struc (stream, offset, self.polygon_desc, obj)
        
    def print_polygon (self, obj):
        self.print_struc (obj, self.polygon_desc)

        
    def read_vertex (self, stream, offset, obj):
        self.read_struc (stream, offset, self.vertex_desc, obj)
        
    def print_vertex (self, obj):
        self.print_struc (obj, self.vertex_desc)

        
        

register_format ('WED', 'V1.3', WED_Format)
