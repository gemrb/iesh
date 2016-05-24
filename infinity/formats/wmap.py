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

# Conforms to IESDP 17.2.2009

from infinity.format import Format, register_format

class WMAP_V10_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },

            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},

            { 'key': 'wmap_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of wmap entries'},

            { 'key': 'wmap_off',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'First wmap entry offset'},
            )


    wmap_desc = (
            { 'key': 'background_image',
              'type': 'RESREF',
              'off': 0x0000,
              'label': 'Background image MOS' },

            { 'key': 'width',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Width' },

            { 'key': 'height',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Height' },

            { 'key': 'map_num',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Map number' },

            { 'key': 'area_name',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Area name' },

            { 'key': 'unknown_18',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'Unknown 18' },

            { 'key': 'unknown_1C',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Unknown 1C' },

            { 'key': 'area_cnt',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Num of area entries' },

            { 'key': 'area_off',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Offset of first area entry' },

            { 'key': 'area_link_off',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Offset of first area link entry' },

            { 'key': 'area_link_cnt',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Num of area link entries' },

            { 'key': 'map_icon_resref',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Map icons BAM resref' },

            { 'key': 'unknown_38',
              'type': 'BYTES',
              'off': 0x0038,
              'size': 128,
              'label': 'Unknown 38' },
            )

    area_desc = (
            { 'key': 'area_resref',
              'type': 'RESREF',
              'off': 0x0000,
              'label': 'Area resref' },

            { 'key': 'area_name',
              'type': 'STR8',
              'off': 0x0008,
              'label': 'Area short name' },

            { 'key': 'area_long_name',
              'type': 'STR32',
              'off': 0x0010,
              'label': 'Area long name' },

            { 'key': 'area_status',
              'type': 'DWORD',
              'off': 0x0030,
              'mask': { 0x01: 'Visible',  0x02: 'Visible from adjacent',  0x04: 'Reachable',  0x08: 'Already visited' },
              'label': 'Area status flags' },

            { 'key': 'icon_seq_ndx',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Icon BAM sequence index' },

            { 'key': 'xpos',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'X coordinate on world map' },

            { 'key': 'ypos',
              'type': 'DWORD',
              'off': 0x003C,
              'label': 'Y coordinate on world map' },

            { 'key': 'area_name_caption',
              'type': 'STRREF',
              'off': 0x0040,
              'label': 'Area title for captions' },

            { 'key': 'area_name_tooltip',
              'type': 'STRREF',
              'off': 0x0044,
              'label': 'Area title for tooltips' },

            { 'key': 'loading_screen',
              'type': 'RESREF',
              'off': 0x0048,
              'label': 'Loading screen MOS file' },


            { 'key': 'area_link_north_ndx',
              'type': 'DWORD',
              'off': 0x0050,
              'label': 'Index of 1st area link north' },

            { 'key': 'area_link_north_cnt',
              'type': 'DWORD',
              'off': 0x0054,
              'label': '# of area links north' },


            { 'key': 'area_link_east_ndx',
              'type': 'DWORD',
              'off': 0x0058,
              'label': 'Index of 1st area link east' },

            { 'key': 'area_link_east_cnt',
              'type': 'DWORD',
              'off': 0x005C,
              'label': '# of arealinks east' },


            { 'key': 'area_link_south_ndx',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Index of 1st area link south' },

            { 'key': 'area_link_south_cnt',
              'type': 'DWORD',
              'off': 0x0064,
              'label': '# of area links south' },


            { 'key': 'area_link_west_ndx',
              'type': 'DWORD',
              'off': 0x0068,
              'label': 'Index of 1st arealink west' },

            { 'key': 'area_link_west_cnt',
              'type': 'DWORD',
              'off': 0x006C,
              'label': '# of area links west' },

            { 'key': 'unknown_70',
              'type': 'BYTES',
              'off': 0x0070,
              'size': 128,
              'label': 'Unknown 70' },

            )

    area_link_desc = (
            { 'key': 'dest_area_ndx',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Destination area index' },

            { 'key': 'entry_point',
              'type': 'STR32',
              'off': 0x0004,
              'label': 'Destination area entry point name' },

            { 'key': 'travel_time',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Travel time / 4' },

            { 'key': 'default_entry_location',
              'type': 'DWORD',
              'off': 0x0028,
              'enum': { 1: 'North', 2: 'East',  4: 'South',  8: 'West'},  # FIXME: looks like mask, not enum
              'label': 'Default entry location' },

            { 'key': 'encounter_area0',
              'type': 'RESREF',
              'off': 0x002C,
              'label': 'Area of random encounter 0' },

            { 'key': 'encounter_area1',
              'type': 'RESREF',
              'off': 0x0034,
              'label': 'Area of random encounter 1' },

            { 'key': 'encounter_area2',
              'type': 'RESREF',
              'off': 0x003C,
              'label': 'Area of random encounter 2' },

            { 'key': 'encounter_area3',
              'type': 'RESREF',
              'off': 0x0044,
              'label': 'Area of random encounter 3' },

            { 'key': 'encounter_area4',
              'type': 'RESREF',
              'off': 0x004C,
              'label': 'Area of random encounter 4' },

            { 'key': 'encounter_chance',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Random encounter chance' },

            { 'key': 'unknown_58',
              'type': 'BYTES',
              'off': 0x0058,
              'size': 128,
              'label': 'Unknown 58' },

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'WMAP'

        self.wmap_list = []

        # FIXME: they should be local to wmap entries
        self.area_list = []
        self.area_link_list = []




    def read (self, stream):
        self.read_header (stream)

        size_area = self.get_struc_size (self.area_desc)
        size_area_link = self.get_struc_size (self.area_link_desc)

        self.read_list (stream,  'wmap')

        for wmap in self.wmap_list:
            off = wmap['area_off']
            for i in range (wmap['area_cnt']):
                obj = {}
                self.read_struc (stream, off, self.area_desc, obj)
                self.area_list.append (obj)
                off += size_area

            off = wmap['area_link_off']
            for i in range (wmap['area_link_cnt']):
                obj = {}
                self.read_struc (stream, off, self.area_link_desc, obj)
                self.area_link_list.append (obj)
                off += size_area_link


    def printme (self):
        self.print_header ()

        self.print_list ('wmap')
        self.print_list ('area')
        self.print_list ('area_link')


register_format (WMAP_V10_Format, signature='WMAPV1.0', extension='WMP', name=('WMP', 'WMAP', 'WORLDMAP'), type=0x3f7)
