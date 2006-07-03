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

# RCS: $Id: dlg.py,v 1.1 2006/07/03 18:15:35 edheldil Exp $

from format import Format, register_format, core

class DLG_Format (Format):
    def __init__ (self, filename):
        Format.__init__ (self, filename)
        self.expect_signature = 'DLG'

        self.state_list = []
        self.transition_list = []
        self.state_trigger_list = []
        self.transition_trigger_list = []
        self.action_list = []


        self.header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'state_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Number of states'},

            { 'key': 'state_off',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'State table offset'},

            { 'key': 'transition_cnt',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Number of transitions'},

            { 'key': 'transition_off',
              'type': 'DWORD',
              'off': 0x0014,
              'label': 'Transition table offset'},


            { 'key': 'state_trigger_off',
              'type': 'DWORD',
              'off': 0x0018,
              'label': 'State trigger table offset'},

            { 'key': 'state_trigger_cnt',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Number of state triggers'},


            { 'key': 'transition_trigger_off',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Transition trigger table offset'},

            { 'key': 'transition_trigger_cnt',
              'type': 'DWORD',
              'off': 0x0024,
              'label': 'Number of transition triggers'},


            { 'key': 'action_off',
              'type': 'DWORD',
              'off': 0x0028,
              'label': 'Action table offset'},

            { 'key': 'action_cnt',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Number of actions'},

            )

        self.state_desc = (
            { 'key': 'npc_text',
              'type': 'STRREF',
              'off': 0x0000,
              'label': 'NPC text'},

            { 'key': 'first_transition_index',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'First transition index'},

            { 'key': 'transition_cnt',
              'type': 'DWORD',
              'off': 0x0008,
              'label': 'Number of transitions'},

            { 'key': 'trigger_index',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Trigger'},

            )


        self.transition_desc = (
            { 'key': 'flags',
              'type': 'DWORD',
              'mask': {0x01:'has text', 0x02:'has trigger', 0x04:'has action', 0x08:'terminates dlg', 0x10:'journal entry', 0x20:'unknown', 0x40:'add quest journal', 0x80:'del quest journal', 0x100:'add done quest journal'},
              'off': 0x0000,
              'label': 'Flags'},

            { 'key': 'pc_text',
              'type': 'STRREF',
              'off': 0x0004,
              'label': 'PC text'},

            { 'key': 'journal_text',
              'type': 'STRREF',
              'off': 0x0008,
              'label': 'Journal text'},

            { 'key': 'trigger_index',
              'type': 'DWORD',
              'off': 0x000C,
              'label': 'Trigger'},

            { 'key': 'action_index',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Action'},

            { 'key': 'next_dialog',
              'type': 'RESREF',
              'off': 0x0014,
              'label': 'Next dialog resref'},

            { 'key': 'next_state',
              'type': 'DWORD',
              'off': 0x001C,
              'label': 'Next state'},

            )
        
        self.script_desc = (
            { 'key': 'script_off',
              'type': 'DWORD',
              'off': 0x0000,
              'label': 'Script offset'},

            { 'key': 'script_len',
              'type': 'DWORD',
              'off': 0x0004,
              'label': 'Script size'},
            
            { 'key': 'code',
              'type': '_STRING',
              'off': 0x0000,
              'label': 'Script code'},
            
            )



    def decode_file (self):
        self.decode_header ()

        off = self.header['state_off']
        for i in range (self.header['state_cnt']):
            obj = {}
            self.decode_state (off, obj)
            self.state_list.append (obj)
            off = off + 16

        off = self.header['transition_off']
        for i in range (self.header['transition_cnt']):
            obj = {}
            self.decode_transition (off, obj)
            self.transition_list.append (obj)
            off = off + 32


        off = self.header['state_trigger_off']
        for i in range (self.header['state_trigger_cnt']):
            obj = {}
            self.decode_script (off, obj)
            self.state_trigger_list.append (obj)
            off = off + 8

        off = self.header['transition_trigger_off']
        for i in range (self.header['transition_trigger_cnt']):
            obj = {}
            self.decode_script (off, obj)
            self.transition_trigger_list.append (obj)
            off = off + 8

        off = self.header['action_off']
        for i in range (self.header['action_cnt']):
            obj = {}
            self.decode_script (off, obj)
            self.action_list.append (obj)
            off = off + 8


#         off = self.header['feature_block_off'] + self.header['casting_feature_block_off'] * 48
#         for i in range (self.header['casting_feature_block_cnt']):
#             obj = {}
#             self.decode_feature_block (off, obj)
#             self.casting_feature_block_list.append (obj)
#             off = off + 48


    def print_file (self):
        self.print_header ()

        i = 0
        for obj in self.state_list:
            print 'State #%d' %i
            self.print_state (obj)
            i = i + 1

        i = 0
        for obj in self.transition_list:
            print 'Transition #%d' %i
            self.print_transition (obj)
            i = i + 1

        i = 0
        for obj in self.state_trigger_list:
            print 'State trigger#%d' %i
            self.print_script (obj)
            i = i + 1

        i = 0
        for obj in self.transition_trigger_list:
            print 'Transition trigger #%d' %i
            self.print_script (obj)
            i = i + 1

        i = 0
        for obj in self.action_list:
            print 'Action #%d' %i
            self.print_script (obj)
            i = i + 1




    def decode_header (self):
        self.header = {}
        self.decode_by_desc (0x0000, self.header_desc, self.header)
        
    def print_header (self):
        self.print_by_desc (self.header, self.header_desc)
        

    def decode_state (self, offset, obj):
        self.decode_by_desc (offset, self.state_desc, obj)

    def decode_transition (self, offset, obj):
        self.decode_by_desc (offset, self.transition_desc, obj)

    def decode_script (self, offset, obj):
        self.decode_by_desc (offset, self.script_desc, obj)

        obj['code'] = self.stream.decode_sized_string (obj['script_off'], obj['script_len'])
        obj['code_raw'] = obj['code']
        #if core.lang_trans:
        #    obj['code'] = string.translate (obj['code'], core.lang_trans)


#         obj['feature_list'] = []
#         off2 = self.header['feature_block_off'] + obj['feature_off'] * 48
#         for j in range (obj['feature_cnt']):
#             obj2 = {}
#             self.decode_feature_block (off2, obj2)
#             obj['feature_list'].append (obj2)
#             off2 = off2 + 48
            
    def print_state (self, obj):
        self.print_by_desc (obj, self.state_desc)

    def print_transition (self, obj):
        self.print_by_desc (obj, self.transition_desc)

    def print_script (self, obj):
        self.print_by_desc (obj, self.script_desc)


    def print_flow (self):
        i = 0
        for state in self.state_list:
            print 'State %d:' %i
            #self.print_state (state)
            if (state['trigger_index'] != 0xffffffff):
                print '  Trigger:', self.state_trigger_list[state['trigger_index']]['code']
            if core.strrefs:
                print '  Text:', core.strrefs.strref_list[state['npc_text']]['string']
            else:
                print '  Text:', state['npc_text']

            j = 0
            for transition in self.transition_list[state['first_transition_index']:state['first_transition_index']+state['transition_cnt']]:
                print '\n  Trans %d:' %j
                if (transition['flags'] & 0x02) and transition['trigger_index'] != 0xffffffff:
                    print '    Trigger:', self.transition_trigger_list[transition['trigger_index']]['code']

                if (transition['flags'] & 0x01) and transition['pc_text'] != 0xffffffff:
                    if core.strrefs:
                        print '    Text:', core.strrefs.strref_list[transition['pc_text']]['string']
                    else:
                        print '  Text:', transition['pc_text']

                if (transition['flags'] & 0x04) and transition['action_index'] != 0xffffffff:
                    print '    Action:', self.action_list[transition['action_index']]['code']

                if not (transition['flags'] & 0x08):
                    print '    ->', transition['next_dialog'], ":", transition['next_state']
                else:
                    print '    -> FIN'

                print "\n"
                j = j + 1
                
            i = i + 1

        
register_format ('DLG', 'V1.0', DLG_Format)
