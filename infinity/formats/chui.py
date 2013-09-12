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

# Conforms to IELister 40d421d0c87c570434ae5e46f4ea60703ac70671


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
          'type': 'DWORD',
          'off': 0x0000,
          'label': 'Window id' },

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
          'label': 'Background MOS' },

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
                   1: 'progressbar',
                   2: 'slider',
                   3: 'textedit',
                   5: 'textarea',
                   6: 'label',
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
          'label': 'Pixmap BAM' },

        { 'key': 'bam_cycle', # FIXME: ielister has alignment & cycle!!!
          'type': 'BYTE',
          'off': 0x0016,
          'label': 'Cycle in BAM file' },

        { 'key': 'justification',
          'type': 'BYTE',
          'off': 0x0017,
          'mask': { 0x01: 'left', 0x02: 'right', 0x04: 'top', 0x08: 'bottom', 0x10: 'anchor', 0x20: 'reduce size', 0x40: 'nowrap', 0x80: 'unknown7'},
          'label': 'Button text justification' },

        { 'key': 'frame_unpressed',
          'type': 'BYTE',
          'off': 0x0018,
          'label': 'BAM frame: button unpressed' },

        { 'key': 'frame_pressed',
          'type': 'BYTE',
          'off': 0x001A,
          'label': 'BAM frame: button pressed' },

        { 'key': 'frame_selected',
          'type': 'BYTE',
          'off': 0x001C,
          'label': 'BAM frame: button selected' },

        { 'key': 'frame_disabled',
          'type': 'BYTE',
          'off': 0x001E,
          'label': 'BAM frame: button disabled' },

        { 'key': 'anchor_x_lsb',
          'type': 'BYTE',
          'off': 0x0019,
          'label': 'Anchor X lsb' },

        { 'key': 'anchor_x_msb',
          'type': 'BYTE',
          'off': 0x001B,
          'label': 'Anchor X msb' },

        { 'key': 'anchor_y_lsb',
          'type': 'BYTE',
          'off': 0x001D,
          'label': 'Anchor Y lsb' },

        { 'key': 'anchor_y_msb',
          'type': 'BYTE',
          'off': 0x001F,
          'label': 'Anchor Y msb' },

        )

    control_progressbar_record_desc = (
        { 'key': 'background',
          'type': 'RESREF',
          'off': 0x000E,
          'label': 'Background' },

        { 'key': 'slider',
          'type': 'RESREF',
          'off': 0x0016,
          'label': 'Cycle in BAM file' },

        { 'key': 'bam',
          'type': 'RESREF',
          'off': 0x001E,
          'label': 'BAM' },

        { 'key': 'stepcount',
          'type': 'WORD',
          'off': 0x0026,
          'label': 'Stepcount' },

        { 'key': 'cycle',
          'type': 'WORD',
          'off': 0x0028,
          'label': 'Cycle' },

        { 'key': 'knob_position',
          'type': 'POINT',
          'off': 0x002A,
          'label': 'Knob position' },

        { 'key': 'cap_position',
          'type': 'POINT',
          'off': 0x002E,
          'label': 'Cap position' },
        )
    
    control_slider_record_desc = (
        { 'key': 'background',
          'type': 'RESREF',
          'off': 0x000E,
          'label': 'Background MOS' },

        { 'key': 'slider',
          'type': 'RESREF',
          'off': 0x0016,
          'label': 'Slider BAM' },

        { 'key': 'bam_cycle',
          'type': 'WORD', # FIXME: iesdp has BYTE here
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

        { 'key': 'unknown2C',
          'type': 'WORD',
          'off': 0x002C,
          'count': 4,
          'label': 'Unknown 2C' },
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
          'label': 'Cursor BAM' },

        { 'key': 'bam_cycle',
          'type': 'WORD', # FIXME: iesdp has unknowns
          'off': 0x002E,
          'label': 'BAM cycle' },

        { 'key': 'frame',
          'type': 'WORD',
          'off': 0x0030,
          'label': 'BAM frame' },

        { 'key': 'position',
          'type': 'POINT',
          'off': 0x0032,
          'label': 'Position' },

        { 'key': 'unknown_36',
          'type': 'DWORD',
          'off': 0x0036,
          'label': 'Unknown 36' },

        { 'key': 'font_file',
          'type': 'RESREF',
          'off': 0x003A,
          'label': 'Font BAM' },

        { 'key': 'unknown_42',
          'type': 'WORD',
          'off': 0x0042,
          'label': 'Unknown 42' },

        { 'key': 'unknown_44',
          'type': 'STR32',
          'off': 0x0044,
          'label': 'Unknown 44' },

        { 'key': 'input_len',
          'type': 'WORD',
          'off': 0x0064,
          'label': 'Max. input length' },

        { 'key': 'uppercase',
          'type': 'DWORD',
          'off': 0x0066,
          'label': 'Uppercase' },
        )

    control_textarea_record_desc = (
        { 'key': 'text_font',
          'type': 'RESREF',
          'off': 0x000E,
          'label': 'Text font BAM' },

        { 'key': 'initials_font',
          'type': 'RESREF',
          'off': 0x0016,
          'label': 'Initials font BAM' },

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
          'label': 'Font BAM' },

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

        offset = self.header['window_offset']
        size_window = self.get_struc_size (self.window_record_desc)
        num_of_controls = 0
        for i in range (self.header['num_of_windows']):
            obj = {}
            self.read_struc (stream, offset, self.window_record_desc, obj)
            self.window_list.append (obj)
            num_of_controls += obj['num_of_controls']
            offset += size_window

        controls = []
        offset = self.header['control_table_offset']
        size_control_table = self.get_struc_size (self.control_table_record_desc)
        for i in range (num_of_controls):
            obj = {}
            self.read_struc (stream, offset, self.control_table_record_desc, obj)
            controls.append(obj)
            offset += size_control_table

        for obj in controls:
            offset = obj['control_offset']
            self.read_control_record(stream, offset, obj)
            
        for obj in self.window_list:
            obj['control_list'] = controls[obj['control_ndx']:obj['control_ndx']+obj['num_of_controls']]          



    def write (self, stream):
        # update
        self.header['window_offset'] = self.get_struc_size (self.header_desc, self.header)
        self.header['num_of_windows'] = len (self.window_list)

        offset = self.header['window_offset']
        controls = []
        for obj in self.window_list:
            offset += self.get_struc_size (self.window_record_desc, obj)
            obj['control_ndx'] = len (controls)
            obj['num_of_controls'] = len (obj['control_list'])
            controls.extend(obj['control_list'])

        self.header['control_table_offset'] = offset
        
        # write
        self.write_header (stream)
        offset = self.header['window_offset']
        for obj in self.window_list:
            self.write_struc (stream, offset, self.window_record_desc, obj)
            offset += self.get_struc_size (self.window_record_desc, obj)

        control_table_record_size = self.get_struc_size (self.control_table_record_desc)
        control_offset = offset + len (controls) * control_table_record_size
        for obj in controls:
            obj['control_offset'] = control_offset
            obj['control_len'] = self.get_control_record_size (obj)
            self.write_struc (stream, offset, self.control_table_record_desc, obj)
            control_offset += obj['control_len']
            offset += control_table_record_size
            
        for obj in controls:
            self.write_control_record(stream, obj['control_offset'], obj)


    def printme (self):
        self.print_header ()

        i = 0
        for obj in self.window_list:
            print('#%d' %i)
            self.print_window_record (obj)
            i = i + 1


    def print_window_record (self, obj):
        self.print_struc (obj, self.window_record_desc)

        j = 0
        for ctl in obj['control_list']:
            print('C #%d' %j)
            self.print_control_record (ctl)
            j = j + 1


    def control_type_to_desc (self, type):
        if type == 0: return self.control_button_record_desc
        elif type == 1: return self.control_progressbar_record_desc
        elif type == 2: return self.control_slider_record_desc
        elif type == 3: return self.control_textedit_record_desc
        elif type == 5: return self.control_textarea_record_desc
        elif type == 6: return self.control_label_record_desc
        elif type == 7: return self.control_scrollbar_record_desc


    def read_control_record (self, stream, offset, obj):
        self.read_struc (stream, offset, self.control_common_record_desc, obj)
        desc = self.control_type_to_desc (obj['type'])
        self.read_struc (stream, offset, desc, obj)


    def write_control_record (self, stream, offset, obj):
        self.write_struc (stream, offset, self.control_common_record_desc, obj)
        desc = self.control_type_to_desc (obj['type'])
        self.write_struc (stream, offset, desc, obj)
        

    def print_control_record (self, obj):
        self.print_struc (obj, self.control_table_record_desc)
        self.print_struc (obj, self.control_common_record_desc)
        desc = self.control_type_to_desc (obj['type'])
        self.print_struc (obj, desc)


    def get_control_record_size (self, obj):
        # NOTE: do not add length of control_common_record_desc, because
        #   it's alread in the specific desc due to its nonzero offset 
        desc = self.control_type_to_desc (obj['type'])
        return self.get_struc_size (desc, obj)

        
register_format (CHUI_Format, signature='CHUIV1  ')
