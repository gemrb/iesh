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


from infinity.format import Format, register_format

class CHUI_Format (Format):
    header_desc = (
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


    window_record_desc = (
        { 'key': 'id',
          'type': 'WORD',
          'off': 0x0000,
          'label': 'Window id' },

        { 'key': 'unknown1',
          'type': 'WORD',
          'off': 0x0002,
          'label': 'Unknown 1' },

        { 'key': 'geometry',
          'type': 'RECT',
          'off': 0x0004,
          'label': 'Window geometry (x,y,w,h)' },

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

    control_table_record_desc = (
        { 'key': 'control_offset',
          'type': 'DWORD',
          'off': 0x0000,
          'label': 'Offset of control'},

        { 'key': 'control_len',
          'type': 'DWORD',
          'off': 0x0004,
          'label': 'Length of control structure'},
        )

    control_common_record_desc = (
        { 'key': 'id',
          'type': 'CTLID',
          'off': 0x0000,
          'label': 'Control ID' },

        { 'key': 'geometry',
          'type': 'RECT',
          'off': 0x0004,
          'label': 'Geometry within window (x,y,w,h)' },

        { 'key': 'type',
          'type': 'BYTE',
          'off': 0x000C,
          'enum': {0: 'button/pixmap',
                   2: 'slider',
                   3: 'textedit',
                   5: 'textarea',
                   6: 'label?',
                   7: 'scrollbar'},
          'label': 'Control type' },

        { 'key': 'unknown',
          'type': 'BYTE',
          'off': 0x000D,
          'label': 'Unknown' },

        )


    control_button_record_desc = (
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

    control_slider_record_desc = (
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

        { 'key': 'knob_position',
          'type': 'POINT',
          'off': 0x0024,
          'label': 'Knob position' },

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

    control_textedit_record_desc = (
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

    control_textarea_record_desc = (
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

    control_label_record_desc = (
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


    control_scrollbar_record_desc = (
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


    def __init__ (self):
        Format.__init__ (self)
        
        self.expect_signature = 'CHUI'
        self.window_list = []



    def read (self, stream):
        self.read_header (stream)

        off = self.header['window_offset']
        for i in range (self.header['num_of_windows']):
            obj = {}
            self.read_window_record (stream, off, obj)
            self.window_list.append (obj)
            off = off + 28

            off2 = self.header['control_table_offset'] + obj['control_ndx'] * 8
            obj['control_list'] = []

            for j in range (obj['num_of_controls']):
                obj2 = {}
                self.read_control_record (stream, off2, obj2)
                obj['control_list'].append (obj2)
                off2 = off2 + 8


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.window_list:
            print '#%d' %i
            self.print_window_record (obj)
            i = i + 1



    def write (self, stream):
        self.header['window_offset'] = self.get_struc_size (self.header_desc, self.header)
        self.header['num_of_windows'] = len (self.window_list)

        offset = self.header['window_offset']
        num_controls = 0
        for obj in self.window_list:
            offset += self.get_struc_size (self.window_record_desc, obj)
            obj['control_ndx'] = num_controls
            obj['num_of_controls'] = len (obj['control_list'])
            num_controls += obj['num_of_controls']
            

        self.header['control_table_offset'] = offset
        

        self.write_struc (stream, 0x0000, self.header_desc, self.header)

        window_offset = self.header['window_offset']
        table_offset = self.header['control_table_offset']
        control_offset = self.header['control_table_offset'] + num_controls * 8
        
        for obj in self.window_list:
            self.write_struc (stream, window_offset, self.window_record_desc, obj)
            window_offset += self.get_struc_size (self.window_record_desc, obj)
            for obj2 in obj['control_list']:
                size = self.write_control (stream, control_offset, obj2)
                obj3 = { 'control_offset': control_offset, 'control_len': size }
                self.write_struc (stream, table_offset, self.control_table_record_desc, obj2)
                control_offset += size
                table_offset += 8  # FIXME
                #xyx()
            

    def read_window_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.window_record_desc, obj)
        
    def print_window_record (self, obj):
        self.print_struc (obj, self.window_record_desc)

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

    def read_control_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.control_table_record_desc, obj)
        off2 = obj['control_offset']
        self.read_struc (stream, off2, self.control_common_record_desc, obj)

        desc = self.control_type_to_desc (obj['type'])
        self.read_struc (stream, off2, desc, obj)


    def write_control (self, stream, offset, obj):
        #print obj
        #size = 0
        #print offset,
        self.write_struc (stream, offset, self.control_common_record_desc, obj)

        #size += self.get_struc_size (self.control_common_record_desc, obj)
        desc = self.control_type_to_desc (obj['type'])
        self.write_struc (stream, offset, desc, obj)
        size = self.get_struc_size (desc, obj)

        return size
        

    def print_control_record (self, obj):
        self.print_struc (obj, self.control_table_record_desc)
        self.print_struc (obj, self.control_common_record_desc)

        desc = self.control_type_to_desc (obj['type'])
        self.print_struc (obj, desc)



    def get_file_res_data (self, obj):
        obj['data'] = self.decode_blob (obj['data_offset'], obj['data_size'])

    def save_file_res (self, filename, obj):
        self.get_file_res_data (obj)
        fh = open (filename, 'w')
        fh.write (obj['data'])
        fh.close ()
        
register_format ('CHUI', 'V1', CHUI_Format)
