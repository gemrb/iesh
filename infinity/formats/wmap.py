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


from infinity.format import Format, register_format

class WMAP_Format (Format):

    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'num_of_wmaps',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of wmap entries'},
            
            { 'key': 'wmap_offset',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'First wmap entry offset'},
            )
        

    wmap_record_desc = (
            { 'key': 'map_resref',
              'type': 'RESREF',
              'off': 0x0000,
              'label': 'Map resource name' },
            
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
            
            { 'key': 'unknown',
              'type': 'DWORD',
              'off': 0x0018,
              'label': '???' },

            { 'key': 'unknown',
              'type': 'DWORD',
              'off': 0x001C,
              'label': '???' },

            { 'key': 'num_of_areas',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Num of area entries' },

            { 'key': 'area_offset',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Offset of first area entry' },

            { 'key': 'arealink_offset',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Offset of first arealink entry' },

            { 'key': 'num_of_arealinks',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Num of arealink entries' },

            { 'key': 'map_icon_resref',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Map icons resource name' },
            
            { 'key': 'unknown38',
              'type': 'BYTES',
              'off': 0x0038,
              'size': 128,
              'label': 'Unknown 0x0038' },
            )

    area_record_desc = (
            { 'key': 'area_name',
              'type': 'RESREF',
              'off': 0x0000,
              'label': 'Area name' },
            
            { 'key': 'area_resref',
              'type': 'RESREF',
              'off': 0x0008,
              'label': 'Area resref' },
            
            { 'key': 'area_long_name',
              'type': 'STR32',
              'off': 0x0010,
              'label': 'Area long name' },
            
            { 'key': 'area_status',
              'type': 'DWORD',
              'off': 0x0030,
              'label': 'Area status flags' },
            
            { 'key': 'icon_seq_ndx',
              'type': 'DWORD',
              'off': 0x0034,
              'label': 'Icon sequence index' },
            
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
            

            { 'key': 'arealink_ndx_north',
              'type': 'DWORD',
              'off': 0x0050,
              'label': 'Index of 1st arealink north' },

            { 'key': 'arealinks_cnt_north',
              'type': 'DWORD',
              'off': 0x0054,
              'label': '# of arealinks north' },


            { 'key': 'arealink_ndx_east',
              'type': 'DWORD',
              'off': 0x0058,
              'label': 'Index of 1st arealink east' },

            { 'key': 'arealinks_cnt_east',
              'type': 'DWORD',
              'off': 0x005C,
              'label': '# of arealinks east' },


            { 'key': 'arealink_ndx_south',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Index of 1st arealink south' },

            { 'key': 'arealinks_cnt_south',
              'type': 'DWORD',
              'off': 0x0064,
              'label': '# of arealinks south' },


            { 'key': 'arealink_ndx_west',
              'type': 'DWORD',
              'off': 0x0068,
              'label': 'Index of 1st arealink west' },

            { 'key': 'arealinks_cnt_west',
              'type': 'DWORD',
              'off': 0x006C,
              'label': '# of arealinks west' },

            { 'key': 'unknown70',
              'type': 'BYTES',
              'off': 0x0070,
              'size': 128,
              'label': 'Unknown 0x0070' },

            )

    arealink_record_desc = (
            { 'key': 'dest_map_ndx',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Destination map index' },

            { 'key': 'dest_map_entry_point',
              'type': 'STR32',
              'off': 0x0004,
              'label': 'Destination map entry_point name' },

            { 'key': 'distance_scale',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Distance scale?' },

            { 'key': 'flags',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Flags' },

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

            { 'key': 'unknown58',
              'type': 'BYTES',
              'off': 0x0058,
              'size': 128,
              'label': 'Unknown 0x0058' },

            )

    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'WMAP'

        self.wmap_list = []

        # FIXME: maybe they should be local to wmap entries
        self.area_list = []
        self.arealink_list = []




    def read (self, stream):
        self.read_header (stream)

        off = self.header['wmap_offset']
        print self.get_struc_size (self.wmap_record_desc)
        print self.get_struc_size (self.area_record_desc)
        print self.get_struc_size (self.arealink_record_desc)
        
        for i in range (self.header['num_of_wmaps']):
            obj = {}
            self.read_wmap_record (stream, off, obj)
            self.wmap_list.append (obj)
            off = off + 184#self.get_struc_size (self.wmap_record_desc) # FIXME: compute the size outside the loop

        for wmap in self.wmap_list:
            off = wmap['area_offset']
            for i in range (wmap['num_of_areas']):
                obj = {}
                self.read_area_record (stream, off, obj)
                self.area_list.append (obj)
                off = off + 240#self.get_struc_size (self.area_record_desc) # FIXME: compute the size outside the loop

            off = wmap['arealink_offset']
            for i in range (wmap['num_of_arealinks']):
                obj = {}
                self.read_arealink_record (stream, off, obj)
                self.arealink_list.append (obj)
                # FIXME: is the size correct???
                off = off + 168#self.get_struc_size (self.arealink_record_desc) # FIXME: compute the size outside the loop

    def printme (self):
        self.print_header ()

        self.print_list ('wmap')
        self.print_list ('arealink')
        self.print_list ('area')





register_format ('WMAP', 'V1.0', WMAP_Format)
