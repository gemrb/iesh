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

import re

from infinity import core
from infinity.format import Format, register_format


class BAF_Format (Format):
    fn_spec_re = re.compile ('([A-Za-z0-9_]+)\s*\((.*)\)')

    def __init__ (self):
        self.c = None
        self.token = None
        self.lineno = 1
        self.ids_codes = {}


    def read_token (self, stream):
        def getc ():
            if self.c is None:
                return stream.get_char ()
            else:
                c = self.c
                self.c = None
                return c

        def nextc ():
            if self.c is None:
                self.c = stream.get_char ()
                return self.c
            else:
                return self.c

        # Skip over spaces and newlines
        c = getc ()
        while c.isspace ():
            if c == "\n":
                self.lineno += 1
            c = getc ()

        if c == '':
            return None
            
        elif c == '[':
            res = c
            while True:
                c = getc ()
                res = res + c
                if c == ']':
                    break
            return res
            
        elif c == '"':
            res = c
            while True:
                c = getc ()
                res = res + c
                if c == '"':
                    break
            return res
            
        elif c in ['#', '(', ')', ',']:
            return c
    
        elif c.isdigit () or (c == '-' and nextc ().isdigit ()):
            if c == '-':
                signum = -1
                c = getc ()
            else:
                signum = 1
                
            res = c
            while nextc ().isdigit ():
                res = res + getc ()
            res = signum * int (res)
            return res

        elif c.isupper ():
            res = c
            while nextc ().isalpha ():
                res = res + getc ()
            return res

        else:
            raise ValueError ("Unknown token: %s (at line %d)" %(c, self.lineno))


    def get_token (self, stream):
        if self.token is None:
            tok = self.read_token (stream)
            p='.'
        else:
            tok = self.token
            self.token = None
            p='x'

        print '>>' + p+':'+repr(tok) + '<<'
        return tok

    def next_token (self, stream):
            if self.token is None:
                self.token = self.read_token (stream)
                return self.token
            else:
                return self.token

    def expect_token (self, stream, tok):
        rtok = self.get_token (stream)
        if rtok != tok:
            raise ValueError ("Expected %s, got %s (at line %d)" %(tok, str (rtok), self.lineno))
        return rtok


    def read (self, stream):
        obj = []

        while self.next_token (stream) != None:
            obj.append (self.read_condition_response_block (stream))

        self.script = obj
        return self

    def read_condition_response_block (self, stream):
        ### <CR> -> CR <CRtail>
        ### <CRtail> -> <CO> <RS> <CRtail>
        ### <CRtail> -> CR
        
        obj = []
        
        self.expect_token (stream, 'IF')
        obj.append (self.read_condition (stream))
        self.expect_token (stream, 'THEN')
        obj.append (self.read_response_set (stream))
        self.expect_token (stream, 'END')
        
#        obj.append (self.expect_token (stream, 'CR'))
#        while self.next_token (stream) == 'CO':
#            obj.append (self.read_condition (stream))
#            obj.append (self.read_response_set (stream))
#        self.expect_token (stream, 'CR')
    
        return obj


    def read_condition (self, stream):
        ### <CO> -> CO <COtail>
        ### <COtail> -> <TR> <COtail>
        ### <COtail> -> CO

        obj = []

        while self.next_token (stream) != 'THEN':
            obj.append (self.read_trigger (stream))


#        obj.append (self.expect_token (stream, 'CO'))
#        while self.next_token (stream) == 'TR':
#            obj.append (self.read_trigger (stream))
#        self.expect_token (stream, 'CO')
        
        return obj

    def read_trigger (self, stream):
        obj = []
        
        obj.append (self.get_token (stream))
        self.expect_token (stream, '(')
        while self.next_token (stream) != ')':
            obj.append (self.get_token (stream))
            if self.next_token (stream) != ')':
                self.expect_token (stream, ',')

        self.expect_token (stream, ')')

#        # pst:  id, 4*I, point, 2*S, O
#        # FIXME: not correct, one of the ints is flags field
#        
#        obj.append (self.expect_token (stream, 'TR'))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.read_object (stream))
#        self.expect_token (stream, 'TR')
#        
#        self.add_ids_code('TRIGGER', obj[1])
#        #print core.id_to_symbol ('TRIGGER', obj[1])
        return obj

    def read_response_set (self, stream):
        ### <RS> -> RS <RStail>
        ### <RStail> -> <RE> <RStail>
        ### <RStail> -> RS

        obj = []
        
        while self.next_token (stream) == 'RESPONSE':
            obj.append (self.read_response (stream))

                
#        obj.append (self.expect_token (stream, 'RS'))
#        while self.next_token (stream) == 'RE':
#            obj.append (self.read_response (stream))
#        self.expect_token (stream, 'RS')
        
        return obj
    
    def read_response (self, stream):
        ### <RE> -> RE int <AC> <REtail>
        ### <REtail> -> <AC> <REtail>
        ### <REtail> -> RE
        # FIXME: this is different from what is described in IESDP, where
        #   each response has only one action, but e.g. look at PST's 0202FD1.BCS
        
        obj = []
        self.expect_token (stream, 'RESPONSE')
        self.expect_token (stream, '#')
        obj.append (self.get_token (stream))
        
        while self.next_token (stream) != 'RESPONSE' and self.next_token (stream) != 'END':
            obj.append (self.read_action (stream))
                
#        obj.append (self.expect_token (stream, 'RE'))
#        obj.append (self.get_token (stream))
#        while self.next_token (stream) == 'AC':
#            obj.append (self.read_action (stream))
#        self.expect_token (stream, 'RE')
        
        return obj
    
    def read_action (self, stream):
        obj = []

        obj.append (self.get_token (stream))
        self.expect_token (stream, '(')
        args = self.read_action_args (stream)
        self.expect_token (stream, ')')
        obj.append (args)

        #pst:  id, 3*O, 5*I, 2*S
#        obj.append (self.expect_token (stream, 'AC'))
#        obj.append (self.get_token (stream))
#        obj.append (self.read_object (stream))
#        obj.append (self.read_object (stream))
#        obj.append (self.read_object (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        self.expect_token (stream, 'AC')
#        self.add_ids_code('ACTION', obj[1])
        return obj
    
    def read_action_args (self, stream):
        obj = []
        while self.next_token (stream) != ')':
            tok = self.get_token (stream)
            args = None
            if self.next_token (stream) == '(':
                self.expect_token (stream, '(')
                args = self.read_action_args (stream)
                self.expect_token (stream, ')')
            obj.append ((tok, args))
            if self.next_token (stream) == ',':
                self.expect_token (stream, ',')
            elif self.next_token (stream) == ')':
                pass
            else:
                raise ValueError ("Expected ) or ,") 
        return obj
                
    
#    def read_object (self, stream):
#        obj = []
#        # PST: id, 13*I, rect, S 
#        obj.append (self.expect_token (stream, 'OB'))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        #print obj
#        #if self.next_token (stream) == 'OB':
#        #    print "short object"
#        #    self.get_token (stream)
#        #    return obj
#            
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        obj.append (self.get_token (stream))
#        self.expect_token (stream, 'OB')
#        
#        #print core.id_to_symbol ('OBJECT', obj[10])
#        return obj

    def printme (self):
        odef = {
                'pst_tr': {
                           'id': (0,),
                           'I': (1, 3),
                           'not': (2,),
                           'P': (5,),
                           'S': (6,7),
                           'O': (8,),
                           },
                'pst_ac': {
                           'id': (0,),
                           'O': (2,3,1),
                           'I': (4, 7, 8),
                           'P': (5,), # actually, it consists of two integers
                           'S': (9, 10),
                           },
                }
        
        # FIXME: globalsetglobal, globalorglobal, ...
        split_string_fns = ('global', 
                                    'globalgt', 
                                    'globallt', 
                                    'globalband',
                                    'globalbor',
                                    'globalmin',
                                    'globalmax',
                                    'globalshl',
                                    'globalshr',
                                    'globalxor',
                                    'bitcheck', 
                                    'bitcheckexact',
                                    
                                    'globalset', 
                                    'setglobal', 
                                    'incrementglobal', 
                                    'bitset', 
                                    'bitclear')
        
        game_type = 'pst'

        def resolve_object (obj):
            res = []
            if obj[1] != 0:
                res.append (core.id_to_symbol ('EA', obj[1]))
            if obj[2] != 0:
                res.append (core.id_to_symbol ('FACTION', obj[2]))
            if obj[3] != 0:
                res.append (core.id_to_symbol ('TEAM', obj[3]))
            if obj[4] != 0:
                res.append (core.id_to_symbol ('GENERAL', obj[4]))
            if obj[5] != 0:
                res.append (core.id_to_symbol ('RACE', obj[5]))
            if obj[6] != 0:
                res.append (core.id_to_symbol ('CLASS', obj[6]))
            if obj[7] != 0:
                res.append (core.id_to_symbol ('SPECIFIC', obj[7]))
            if obj[8] != 0:
                res.append (core.id_to_symbol ('GENDER', obj[8]))
            if obj[9] != 0:
                res.append (core.id_to_symbol ('ALIGNMEN', obj[9]))

            if res:
                res = '[' + '.'.join (res) + ']'
            else:
                res = None

            res2 = None
            if obj[10] != 0:
                res2 = core.id_to_symbol ('OBJECT', obj[10])
            if obj[11] != 0:
                res2 = core.id_to_symbol ('OBJECT', obj[11]) + '(' + res2 +')'
            if obj[12] != 0:
                res2 = core.id_to_symbol ('OBJECT', obj[12]) + '(' + res2 +')'
            if obj[13] != 0:
                res2 = core.id_to_symbol ('OBJECT', obj[13]) + '(' + res2 +')'
            if obj[14] != 0:
                res2 = core.id_to_symbol ('OBJECT', obj[14]) + '(' + res2 +')'
                
            # FIXME: what about area?? [-1.-1.-1.-1] (15)
            res3 = None
            if obj[16] != '""':
                res3 = obj[16]

            if (res and res2) or (res and res3) or (res2 and res3):
                raise ValueError ("Error: More values for object: " + repr (res) + '//' + repr (res2) + '//' + repr (res3))
                
            if res:
                return res
            elif res2:
                return res2
            elif res3:
                return res3
            else:
                return "'OBJ"


        def resolve_args (fn_spec, obj_type, obj):
            mo = self.fn_spec_re.match (fn_spec)
            fn_name = mo.groups ()[0]
            args = mo.groups ()[1].split (",")
            arg_indices = {}
            res_args = []
            
            split_string_arg = fn_name.lower () in  split_string_fns

            for arg in args:
                #print 'arg', fn_spec, arg
                if arg == '':
                    break
                type, name = arg.split (':')
                name, file = name.split ('*')
                
                if arg_indices.has_key (type):
                    arg_indices[type] = index = arg_indices[type] + 1
                else:
                    arg_indices[type] = index = 0

                #print 'ot:', obj_type, 'type;', type, 'index:', index
                if not split_string_arg or type != 'S' or index == 0:
                    aindex = odef[game_type + '_' + obj_type][type][index] + 1
                else:
                    aindex = odef[game_type + '_' + obj_type][type][index-1] + 1
                    
                
                if type == 'I':
                    v = str (obj[aindex])
                    #print 'Lookup', file, tr[index + 1]
                    if file:
                        v = core.id_to_symbol (file, obj[aindex])
                    res_args.append (v)

                elif type == 'P':
                    res_args.append ('[%d.%d]' %(obj[aindex], obj[aindex+1]))

                elif type == 'S':
                    if split_string_arg:
                        if index == 0:
                            res_args.append ('"' + obj[aindex][7:])
                            res_args.append (obj[aindex][0:7] + '"')
                        elif index == 1:
                            pass
                        else:
                            res_args.append (obj[aindex])
                    else:
                        res_args.append (obj[aindex])
    
                elif type == 'O':
                    res_args.append (resolve_object (obj[aindex]))

            return fn_name, res_args

        def resolve_action (ac):
            res = str (ac[0])
            if ac[1] is not None:
                args = [ resolve_action (arg)  for arg in ac[1] ]
                res += '(' + ','.join (args) + ')'
            return res



        for cr in self.script:
            co = cr[0]
            rs = cr[1]
            print 'IF'
            for tr in co:
                print '    ', tr
                continue
                fn_spec = core.id_to_symbol ('TRIGGER', tr[1])
                neg = ('!', '')[not tr[3]] # FIXME: hack, use odef[]
                
                #print tr_decl
                fn_name, res_args = resolve_args (fn_spec, 'tr', tr)
                print '    ' + neg + fn_name + '(' + ','.join (res_args) + ')'
                #print '    TR', tr_name + '#0x%04x' %tr[1]
            print 'THEN'
            for re in rs:
                print '    RESPONSE #%d' %re[0]
                for ac in re[1:]:
                    #print 'AC', ac[1]
                    print ac, resolve_action (ac)
                    continue
                    fn_spec = core.id_to_symbol ('ACTION', ac[1])
                    fn_name, res_args = resolve_args (fn_spec, 'ac', ac)
                    print '        ' + fn_name + '(' + ','.join (res_args) + ')'
            print 'END\n'


    def add_ids_code (self, ids, id):
        ids = ids.upper ()
        if not self.ids_codes.has_key (ids):
            self.ids_codes[ids] = {}
        if not self.ids_codes[ids].has_key (id):
            self.ids_codes[ids][id] = 1
        else:
            self.ids_codes[ids][id] += 1

    def uses_ids_code (self, ids, code):
        try:
            return self.ids_codes[ids.upper ()][code]
        except:
            return False

    def compile (self):
        obj = []
        obj.append ('SC\n')
        for CR in self.script:
            obj.append ('CR\n')
            # FIXME: can there be really conditions with more than one CO+RS pair?
            CO = CR[0]
            RS = CR[1]
            
            obj.append ('CO\n')
            for TR in CO:
                obj.append ('TR\n')
                obj.extend (TR)
                obj.append ('TR\n')
            obj.append ('CO\n')
            obj.append ('RS\n')
            for RE in RS:
                obj.append ('RE\n')
                obj.append (RE[0])
                for AC in RE[1:]:
                    obj.append ('AC\n')
                    obj.extend (AC)
                    obj.append ('AC\n')
                obj.append ('RE\n')
            obj.append ('RS\n')
            obj.append ('CR\n')
            
        obj.append ('SC\n')
        return obj

register_format ('BAF', '', BAF_Format)
