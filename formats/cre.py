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

# RCS: $Id: cre.py,v 1.1 2005/03/02 20:44:22 edheldil Exp $

from format import Format, register_format

class CRE_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'CRE'

        self.window_list = []


        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'num_of_windows',
              'type': 'DWORD',
              'off': 0x0008,
              'label': '# of windows'},
            
            { 'key': 'control_table_offset',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Control table offset'},

            { 'key': 'window_offset',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'First window offset'},
            )
        

        self.window_record_desc = (
            { 'key': 'id',
              'type': 'WORD',
              'off': 0x0000,
              'label': 'Window id' },
            
            { 'key': 'unknown1',
              'type': 'WORD',
              'off': 0x0002,
              'label': 'Unknown 1' },
            
            { 'key': 'xpos',
              'type': 'WORD',
              'off': 0x0004,
              'label': 'X position' },
            
            { 'key': 'ypos',
              'type': 'WORD',
              'off': 0x0006,
              'label': 'Y position' },
            
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'Width' },
            
            { 'key': 'height',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Height' },
            
            { 'key': 'bg_flag',
              'type': 'WORD',
              'off': 0x000C,
              'label': 'Background flag' },
            
            { 'key': 'num_of_controls',
              'type': 'WORD',
              'off': 0x000E,
              'label': '# of controls' },
            
            { 'key': 'bg_name',
              'type': 'RESREF',
              'off': 0x0010,
              'label': 'Background filename' },

            { 'key': 'control_ndx',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'Index of first control' },

            { 'key': 'unknown2',
              'type': 'WORD',
              'off': 0x001A,
              'label': 'Unknown 2' },
            
            )

        self.control_table_record_desc = (
            { 'key': 'control_offset',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Offset of control'},

            { 'key': 'control_len',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Length of control structure'},
            )

        self.control_common_record_desc = (
            { 'key': 'id',
              'type': 'CTLID',
              'off': 0x0000,
              'label': 'Control ID' },
            
            { 'key': 'xpos',
              'type': 'WORD',
              'off': 0x0004,
              'label': 'X position in window' },
            
            { 'key': 'ypos',
              'type': 'WORD',
              'off': 0x0006,
              'label': 'Y position in window' },
            
            { 'key': 'width',
              'type': 'WORD',
              'off': 0x0008,
              'label': 'Width' },
            
            { 'key': 'height',
              'type': 'WORD',
              'off': 0x000A,
              'label': 'Height' },
            
            { 'key': 'type',
              'type': 'CTLTYPE',
              'off': 0x000C,
              'label': 'Control type' },

            { 'key': 'unknown',
              'type': 'BYTE',
              'off': 0x000D,
              'label': 'Unknown' },

            )


        self.control_button_record_desc = (
            { 'key': 'bam_file',
              'type': 'RESREF',
              'off': 0x000E,
              'label': 'Name of BAM file w/ pixmap' },
            
            { 'key': 'bam_cycle',
              'type': 'BYTE',
              'off': 0x0016,
              'label': 'Cycle in BAM file' },
            
            { 'key': 'justification',
              'type': 'BYTE',
              'off': 0x0017,
              'label': 'Button text justification' },
            
            { 'key': 'frame_unpressed',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'BAM frame: button unpressed' },
            
            { 'key': 'frame_pressed',
              'type': 'WORD',
              'off': 0x001A,
              'label': 'BAM frame: button pressed' },
            
            { 'key': 'frame_selected',
              'type': 'WORD',
              'off': 0x001C,
              'label': 'BAM frame: button selected' },
            
            { 'key': 'frame_disabled',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'BAM frame: button disabled' },
            
            )

        self.control_slider_record_desc = (
            { 'key': 'mos_file',
              'type': 'RESREF',
              'off': 0x000E,
              'label': 'Name of MOS file w/ background' },
            
            { 'key': 'bam_file',
              'type': 'RESREF',
              'off': 0x0016,
              'label': 'Name of BAM file w/ pixmap' },
            
            { 'key': 'bam_cycle',
              'type': 'BYTE',
              'off': 0x001E,
              'label': 'Cycle in BAM file' },
            
            { 'key': 'frame_ungrabbed',
              'type': 'WORD',
              'off': 0x0020,
              'label': 'BAM frame: slider ungrabbed' },
            
            { 'key': 'frame_grabbed',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'BAM frame: slider grabbed' },
            
            { 'key': 'knob_x',
              'type': 'WORD',
              'off': 0x0024,
              'label': 'Knob X offset' },
            
            { 'key': 'knob_y',
              'type': 'WORD',
              'off': 0x0026,
              'label': 'Knob Y offset' },
            
            { 'key': 'knob_jump_width',
              'type': 'WORD',
              'off': 0x0028,
              'label': 'Knob jump width' },
            
            { 'key': 'knob_jump_count',
              'type': 'WORD',
              'off': 0x002A,
              'label': 'Knob jump count' },
            
            { 'key': 'unknown2',
              'type': 'WORD',
              'off': 0x002C,
              'label': 'Unknown 2' },
            
            { 'key': 'unknown3',
              'type': 'WORD',
              'off': 0x002E,
              'label': 'Unknown 3' },
            
            { 'key': 'unknown4',
              'type': 'WORD',
              'off': 0x0030,
              'label': 'Unknown 4' },
            
            { 'key': 'unknown5',
              'type': 'WORD',
              'off': 0x0032,
              'label': 'Unknown 5' },
            
            )

        self.control_textedit_record_desc = (
            { 'key': 'mos_file_1',
              'type': 'RESREF',
              'off': 0x000E,
              'label': 'MOS file 1' },
            
            { 'key': 'mos_file_2',
              'type': 'RESREF',
              'off': 0x0016,
              'label': 'MOS file 2' },
            
            { 'key': 'mos_file_3',
              'type': 'RESREF',
              'off': 0x001E,
              'label': 'MOS file 3' },
            
            { 'key': 'cursor_file',
              'type': 'RESREF',
              'off': 0x0026,
              'label': 'Name of BAM file w/ cursor' },
            
            { 'key': 'unknown2',
              'type': 'BYTES',
              'off': 0x002E,
              'size': 12,
              'label': 'Unknown 2' },
            
            { 'key': 'font_file',
              'type': 'RESREF',
              'off': 0x003A,
              'label': 'Name of BAM file w/ font' },
            
            { 'key': 'unknown3',
              'type': 'BYTES',
              'off': 0x0042,
              'size': 34,
              'label': 'Unknown 3' },

            { 'key': 'input_len',
              'type': 'WORD',
              'off': 0x0064,
              'label': 'Max. input length' },
            
            { 'key': 'unknown4',
              'type': 'DWORD',
              'off': 0x0066,
              'label': 'Unknown 4' },
            
            )

        self.control_textarea_record_desc = (
            { 'key': 'font_file_1',
              'type': 'RESREF',
              'off': 0x000E,
              'label': 'Name of BAM file w/ font 1' },
            
            { 'key': 'font_file_2',
              'type': 'RESREF',
              'off': 0x0016,
              'label': 'Name of BAM file w/ font 2' },
            
            { 'key': 'color_1',
              'type': 'RGBA',
              'off': 0x001E,
              'label': 'Color 1' },
            
            { 'key': 'color_2',
              'type': 'RGBA',
              'off': 0x0022,
              'label': 'Color 2' },
            
            { 'key': 'color_3',
              'type': 'RGBA',
              'off': 0x0026,
              'label': 'Color 3' },
            
            { 'key': 'scrollbar',
              'type': 'DWORD',
              'off': 0x002A,
              'label': 'Scrollbar ID' },
            
            )            

        self.control_label_record_desc = (
            { 'key': 'text',
              'type': 'STRREF',
              'off': 0x000E,
              'label': 'Initial text' },

            { 'key': 'font_file',
              'type': 'RESREF',
              'off': 0x0012,
              'label': 'Name of BAM file w/ font' },
            
            { 'key': 'color_1',
              'type': 'RGBA',
              'off': 0x001A,
              'label': 'Color 1' },
            
            { 'key': 'color_2',
              'type': 'RGBA',
              'off': 0x001E,
              'label': 'Color 2' },
            
            { 'key': 'justification',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'Justification' },
            
            )


        self.control_scrollbar_record_desc = (
            { 'key': 'bam_file',
              'type': 'RESREF',
              'off': 0x000E,
              'label': 'Name of BAM file w/ pixmap' },

            { 'key': 'bam_cycle',
              'type': 'WORD',
              'off': 0x0016,
              'label': 'Cycle in BAM file' },
            
            { 'key': 'frame_up_unpressed',
              'type': 'WORD',
              'off': 0x0018,
              'label': 'BAM frame: up-arrow unpressed' },
            
            { 'key': 'frame_up_pressed',
              'type': 'WORD',
              'off': 0x001A,
              'label': 'BAM frame: up-arrow pressed' },
            
            { 'key': 'frame_down_unpressed',
              'type': 'WORD',
              'off': 0x001C,
              'label': 'BAM frame: down-arrow unpressed' },
            
            { 'key': 'frame_down_pressed',
              'type': 'WORD',
              'off': 0x001E,
              'label': 'BAM frame: down-arrow pressed' },
            
            { 'key': 'frame_trough',
              'type': 'WORD',
              'off': 0x0020,
              'label': 'BAM frame: trough' },
            
            { 'key': 'frame_slider',
              'type': 'WORD',
              'off': 0x0022,
              'label': 'BAM frame: slider' },
            
            { 'key': 'textarea',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Textarea ID' },
            
            )


    def decode_file (self):
        self.decode_header ()

        off = self.header['window_offset']
        for i in range (self.header['num_of_windows']):
            obj = {}
            self.decode_window_record (off, obj)
            self.window_list.append (obj)
            off = off + 28

            off2 = self.header['control_table_offset'] + obj['control_ndx'] * 8
            obj['control_list'] = []

            for j in range (obj['num_of_controls']):
                obj2 = {}
                self.decode_control_record (off2, obj2)
                obj['control_list'].append (obj2)
                off2 = off2 + 8


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.window_list:
            print '#%d' %i
            self.print_window_record (obj)
            i = i + 1


    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_window_record (self, offset, obj):
        self.decode_by_desc (offset, self.window_record_desc, obj)
        
    def print_window_record (self, obj):
        self.print_by_desc (obj, self.window_record_desc)

        j = 0
        for ctl in obj['control_list']:
            print 'C #%d' %j
            self.print_control_record (ctl)
            j = j + 1


    def control_type_to_desc (self, type):
        if type == 0: return self.control_button_record_desc
        elif type == 2: return self.control_slider_record_desc
        elif type == 3: return self.control_textedit_record_desc
        elif type == 5: return self.control_textarea_record_desc
        elif type == 6: return self.control_label_record_desc
        elif type == 7: return self.control_scrollbar_record_desc

    def decode_control_record (self, offset, obj):
        self.decode_by_desc (offset, self.control_table_record_desc, obj)
        off2 = obj['control_offset']
        self.decode_by_desc (off2, self.control_common_record_desc, obj)

        desc = self.control_type_to_desc (obj['type'])
        self.decode_by_desc (off2, desc, obj)

    def print_control_record (self, obj):
        self.print_by_desc (obj, self.control_table_record_desc)
        self.print_by_desc (obj, self.control_common_record_desc)

        desc = self.control_type_to_desc (obj['type'])
        self.print_by_desc (obj, desc)



    def get_file_res_data (self, obj):
        obj['data'] = self.decode_blob (obj['data_offset'], obj['data_size'])

    def save_file_res (self, filename, obj):
        self.get_file_res_data (obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()
        
register_format ('CHUI', 'V1', CHUI_Format)
