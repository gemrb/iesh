#!/usr/bin/env python
from __future__ import print_function

import cPickle
import os.path
import re

import infinity
import infinity.builtins
import infinity.formats.dlg
from infinity import core


class DLGDebugger (object):
    data_dir = '.'
    dlg_ext = '.DLG'

    global_re = '(?i)((!?)([a-z]+)\\s*\\(\\s*(("[^"]+"|-?\\d+|[A-Za-z_][A-Za-z_0-9]*)(\\s*,\\s*("[^"]+"|-?\\d+|[A-Za-z_][A-Za-z_0-9]*)(\\s*,\\s*("[^"]+"|-?\\d+|[A-Za-z_][A-Za-z_0-9]*))?)?)?\\s*\\)\\s*)'

    global_re = re.compile (global_re)

    # "addresses/phases", i.e. where we are in the GET_STATE -> GET_REPLY ->... loop
    A_GET_STATE = 'get_state'
    A_GET_REPLY = 'get_reply'
    A_TRANSITION = 'transition'

    commands = [
        ('env', '', 'print values of known triggers'),
        ('step', '', 'step dialog'),
        ('continue', '', 'continue with dialog'),
        ('run', '', 'rerun the dialog'),
        ('where', '', 'print current dialog, state and phase'),
        ('ps', '[num]', 'print state'),
        ('help', '[cmd]', 'print help on usage or commands'),
        ('quit', '', 'quit the debugger'),
        ]


    def __init__ (self):
        self.reset ()

    def reset (self):
        self.dialogs = {}
        self.values = {}
        self.actions = {}
        self.items = {}
        self.actors = {}


    def get_dialog (self, name):
        if os.path.exists (name):
            resref = os.path.basename (name)
            self.data_dir = os.path.dirname (name)
            try:
                resref,  self.dlg_ext = resref.split (os.path.extsep)
                self.dlg_ext = os.path.extsep + self.dlg_ext
            except:
                self.dlg_ext = ''

            resref = resref.upper ()

        else:
            name = name.upper ()
            resref = name

        #print name, resref
        
        if self.dialogs.has_key (resref):
            return self.dialogs[resref]
        else:
            d = infinity.builtins.load_object (name,  0x3F3)
            self.dialogs[resref] = d
            self.merge_conditions (d)
            d.name = name
            return d

    def parse_condition (self, cond):
        def conv (a):
            if a == '':
                return None
            if len (a) >= 2 and a[0] == '"' and a[-1] == '"':
                return a[1:-1]            
            try:
                return int (a)
            except:
                return a


        #print 'parse:',  cond
        g = DLGDebugger.global_re.findall (cond)
        return map (lambda m: (m[0],  (False,  True)[m[1] == '!'],  m[2].lower(),  conv (m[4]),  conv (m[6]),  conv (m[8])),  g)


    def eval_function (self, cond,  is_merge = False):

        def get_value (key,  default):
            try:
                return self.values[key]
            except KeyError:
                self.values[key] = default
                return default
            
        cond = cond.replace ("\r",  "")
        cond = cond.replace ("\n",  "")

        if cond == '':
            if is_merge:
                return
            else:
                return True


        parsed = self.parse_condition (cond)
        if not parsed:
            if not self.values.has_key (cond):
                self.values[cond] = False
            return
           
        for c in parsed:
            expr = c[0]
            neg = c[1]
            fn = c[2].lower ()
            args = c[3:6]

            #print expr

            if fn in ('global',  'globallt',  'globalgt'):
                key = 'global:' + args[1].upper () + ':' + args[0]
                if is_merge:
                    value = 0
                else:
                    value = self.values[key]
                    if fn == 'global':
                        value = args[2] == value
                    elif fn == 'globallt':
                        value = args[2] > value
                    elif fn == 'globalgt':
                        value = args[2] < value
        
            elif fn == 'globalorglobal':
                key = ['global:' + args[1].upper () + ':' + args[0], 
                            'global:' + args[3].upper () + ':' + args[2]]
                if is_merge:
                    value = [0, 0]
                else:
                    value = self.values[key[0]] or self.values[key[1]]
                    
            elif fn in ('moralelt',  'moralegt'):
                key = 'PC:morale:' + args[0].upper ()
                if is_merge:
                    value = 0
                else:
                    value = self.values[key]
                    if fn == 'moralelt':
                        value = args[2] > value
                    elif fn == 'moralegt':
                        value = args[2] < value
                    
            elif fn in ('partygold', 'partygoldlt',  'partygoldgt'):
                key = 'Party:gold'
                if is_merge:
                    value = 0
                else:
                    value = self.values[key]
                    if fn == 'partygoldlt':
                        value = args[0] > value
                    elif fn == 'partygoldgt':
                        value = args[0] < value
                    else:
                        value = args[0] == value
                    
            elif fn in ('checkstat', 'checkstatlt',  'checkstatgt'):
                key = 'PC:' + args[2].upper () + ':' + args[0].upper ()
                if is_merge:
                    value = 0
                else:
                    value = self.values[key]
                    if fn == 'checkstatlt':
                        value = args[1] > value
                    elif fn == 'checkstatgt':
                        value = args[1] < value
                    else:
                        value = args[1] == value
        
            elif fn in ('proficiency', 'proficiencylt',  'proficiencygt'):
                key = 'PC:proficiency:' + args[0].upper () + ':' + args[1].upper ()
                if is_merge:
                    value = 0
                else:
                    value = self.values[key]
                    if fn.endswith ('lt'):
                        value = args[2] > value
                    elif fn.endswith ('gt'):
                        value = args[2] < value
                    else:
                        value = args[2] == value
        
            elif fn in ('hplt', 'hpgt',  'hppercentlt',  'hppercentgt',  'hppercent'):
                key = ( 'PC:' + args[0].upper () + ':hp',  'PC:' + args[0].upper () + ':hpmax' )
                if is_merge:
                    value = (1, 1)
                else:
                    value = self.values[key[0]]
                    if value == self.values[key[1]]:
                        value2 = 100
                    else:
                        value2 = value / self.values[key[1]]
            
                    if fn == 'hplt':
                        value = value < args[1] 
                    elif fn == 'hpgt':
                        value = value > args[1]
                    elif fn == 'hppercentlt':
                        value = value2 < args[1]
                    elif fn == 'hppecentgt':
                        value = value2 > args[1]
                    elif fn == 'hppercent':
                        value = value2 == args[1]
                
            elif fn == 'class':
                key = 'PC:class:' + args[0].upper ()
                if is_merge:
                    value = args[1].upper ()
                else:
                    value = self.values[key]
                    value = value == args[1].upper ()
        
            elif fn == 'nearbydialog':
                key = 'nearbydialog:' + args[0].upper ()
                if is_merge:
                    value = False
                else:
                    value = self.values[key]
        
            elif fn == 'dead':
                key = 'dead:' + args[0].upper ()
                if is_merge:
                    value = False
                else:
                    value = self.values[key]
        
            elif fn == 'inparty':
                key = 'Party'
                if is_merge:
                    value = []
                else:
                    value = self.values[key]
                    value = args[0].upper() in map (lambda a: a.upper (),  value)

            elif fn in ('partycounteq',  'partycountlt',  'partycountgt'):
                key = 'Party'
                if is_merge:
                    value = []
                else:
                    value = len (values[key])
                    if fn.endswith ('eq'):
                        value = value == args[0]
                    elif fn.endswith ('lt'):
                        value = value < args[0]
                    elif fn.endswith ('gt'):
                        value = value > args[0]

            elif fn == 'hasitem':
                key = 'actor:' + args[1].upper () + ':inv'
                items[args[0]] = 1

                if is_merge:
                    value = {}
                else:
                    value = self.values[key]
                    try:
                        value = value[args[0]]
                    except:
                        value = 0
                    value = value > 0
                    
            elif fn == 'partyhasitem':
                items[args[0]] = 1
                
                if is_merge:
                    key = []
                    value = []
                else:
                    value = False
                    for pc in get_value ('Party',  []):
                        key = 'actor:' + pc.upper () + ':inv'
                        inv = get_value (key,  {})
                        if inv.has_key (args[0]):
                            value = True
                            break
                            
            elif fn in ('partyitemcountlt', 'partyitemcountgt'):
                items[args[0]] = 1
                
                if is_merge:
                    key = []
                    value = []
                else:
                    value = 0
                    for pc in get_value ('Party',  []):
                        key = 'actor:' + pc.upper () + ':inv'
                        inv = get_value (key,  {})
                        if inv.has_key (args[0]):
                            value += inv[args[0]]
                            
                    if fn.endswith ('lt'):
                        value = value < args[1]
                    elif fn.endswith ('gt'):
                        value = value > args[1]
                    
            elif fn == 'true':
                key = 'true'
                value = True
        
            elif fn == 'false':
                key = 'false'
                value = False
        
            else:
                #print 'unrecognized cond:',  expr
                key = expr
                if neg:
                    key = key[1:]
                if is_merge:
                    value = False
                else:
                    value = self.values[key]
        
            if is_merge:
                if type (key) == type (''):
                    key = [ key ]
                    value = [ value ]
                for k in key:
                    if not self.values.has_key (k):
                        self.values[k] = value.pop (0)
            else:
                    if neg:
                        value = not value
                    if not value:
                        return False
        
        if not is_merge:
            return True


    def merge_conditions (self, d):
        for trigger in d.state_trigger_list + d.transition_trigger_list:
            #conditions = trigger['code'].replace("\r",  "\n").split ("\n")
            self.eval_function (trigger['code'],  is_merge = True)

        for action in d.action_list:
            self.actions[action['code']] = 1

    def save_debugger_state (self):
        s = [ dialogs, values, actions ]
        fh = open ("debugger_state.dat",  "w")
        cPickle.dump (s,  fh)
        fh.close ()

    def restore_debugger_state (self):
        global dialogs, values, actions,  items
        
        fh = open ("debugger_state.dat",  "r")
        s = cPickle.load (fh)
        fh.close ()
        dialogs, values, actions  = s


    def merge_all (self):
        def merge_one (d):
            try:
                merge_conditions (d)
            except:
                #print "!!! Merge exception in %s !!!" %d.name
                print("!!! Merge exception !!!")
        
        infinity.builtins.iterate_objects_by_type (0x3f3,  merge_one)

    def print_conditions (self, cond = None):
        if cond is None:
            keys = values.keys ()
            keys.sort ()
        elif values.has_key (cond):
            keys = [ cond ]
        else:
            keys = []
            
        for key in keys:
            print(key,  '=',  repr (values[key]))


    def set_condition_value (self, cond, value = None):
        try:
            oldvalue = values[cond]
        except KeyError:
            # FIXME: maybe try to parse the condition first and test the parsed var?
            print("Condition does not exist:",  cond)
            return
        
        if value == None:
            value = not oldvalue

        values[cond] = value



    def print_state (self, d, state):
        if core.strrefs:
            print('  Text:', core.strrefs.strref_list[state['npc_text']]['string'])
        else:
            print('  Text:', state['npc_text'])

        j = 0
        for transition in d.transition_list[state['first_transition_index']:state['first_transition_index']+state['transition_cnt']]:
            if (transition['flags'] & 0x02) and transition['trigger_index'] != 0xffffffff and not eval_trigger (d.transition_trigger_list[transition['trigger_index']]):
                j += 1
                continue

            print('[%d]' %j, end=' ')
            print_transition (transition)
            j += 1


    def print_transition (self, transition):
    #            if (transition['flags'] & 0x02) and transition['trigger_index'] != 0xffffffff:
    #                print '    Trigger:', self.transition_trigger_list[transition['trigger_index']]['code']

        if (transition['flags'] & 0x01) and transition['pc_text'] != 0xffffffff:
            if core.strrefs:
                print('    ', core.strrefs.strref_list[transition['pc_text']]['string'])
            else:
                print('    ', transition['pc_text'])

    #            if (transition['flags'] & 0x04) and transition['action_index'] != 0xffffffff:
    #                print '    Action:', self.action_list[transition['action_index']]['code']
    #
    #            if not (transition['flags'] & 0x08):
    #                print '    ->', transition['next_dialog'], ":", transition['next_state']
    #            else:
    #                print '    -> FIN'



    def eval_trigger (self, trigger):
        return  eval_function (trigger['code'])


    def get_next_state (self, d, state_ndx = 0):
        while True:
            state = d.state_list[state_ndx]
            if state['trigger_index'] == 0xffffffff or eval_trigger (d.state_trigger_list[state['trigger_index']]):
                return state_ndx
            else:
                state_ndx += 1
                # FIXME: will it end?


    def do_transition (self, d, state, transition_ndx):
        transition = d.transition_list[state['first_transition_index'] + transition_ndx]
        
        if (transition['flags'] & 0x01) and transition['pc_text'] != 0xffffffff:
            if core.strrefs:
                print('SELF:', core.strrefs.strref_list[transition['pc_text']]['string'])
            else:
                print('SELF:', transition['pc_text'])

            if (transition['flags'] & 0x04) and transition['action_index'] != 0xffffffff:
                print('    Exec:', d.action_list[transition['action_index']]['code'])

            if not (transition['flags'] & 0x08):
                print('    ->', transition['next_dialog'], ":", transition['next_state'])
                return transition['next_dialog'], transition['next_state']
            else:
                print('    -> FIN')
                return None,  0

    def parse_cmd (self, cmd):
        cmd = cmd.strip ()
        try:
            cmd,  args = re.split ("\\s+",  cmd,  1)
        except ValueError:
            args = None

        cmd = cmd.lower ()
        
        if cmd == '' and args is None:
            return cmd, args

        if re.match ("^\\d+$", cmd) and args is None:
            return cmd, args

        # Find which command matches user input
        fcmds = []
        for c in DLGDebugger.commands:
            if c[0].startswith (cmd):
                fcmds.append (c[0])
        
        if len (fcmds) == 0:
            print ('Unknown command:', cmd)
            return None, None
        
        elif len (fcmds) > 1:
            print ("Command '%s' may be:", ', '.join (fcmds))
            return None, None

        else:
            cmd = fcmds[0]

        return cmd, args


    def run_dialog (self, name, state = 0):
        global values,  dialogs
        #values = {}
        #dialogs = {}

        # FIXME: this should be made as an extension to  the iesh shell, so
        #   we could type in python commands etc.
        address = DLGDebugger.A_GET_STATE
        step = True

        d = self.get_dialog (name)
        next_dlg = d

        print("\nIE DLG debugger\n")
        print("Type '?' or 'h' to print help on debugger commands\n")


        while True:
            #debugger_shell (name,  state)
            if next_dlg is None:
                d = None
            elif type (next_dlg) == type (""):  
                d = self.get_dialog (name)
            else:
                d = next_dlg

            while step or d is None or address == DLGDebugger.A_GET_REPLY:
                try:
                    cmd = raw_input ('Dbg: ')
                except KeyboardInterrupt:
                    cmd = 'q'
                    print()

                cmd, args = self.parse_cmd (cmd)
                if cmd is None: continue


                if cmd == 'quit':
                    return None,  0
                elif cmd == '':
                    continue
                elif cmd == '?' or cmd == 'help':
                    if args is None:
                        for c in DLGDebugger.commands:
                            print("%-10s\t%-5s\t%s" %(c[0], c[1], c[2]))
                    else:
                        print("help on " + args)
                elif cmd == 'env':
                    if args is None:
                        print_conditions ()
                    else:
                        try:
                            (cond,  value) = re.split('\s*=\s*',  args,  2)
                        except ValueError:
                            cond,  value = args,  None
                        
                        if value is None:
                            print_conditions (cond)
                        else:
                            if value in ('False',  'True'):
                                value = value == 'True'
                            else:
                                try:
                                    value = int (value)
                                except:
                                    pass
        
                            set_condition_value (cond,  value)

                elif cmd == 'ps':
                    if args is None:
                        s = state
                    else:
                        s = int (args[0])

                    print("State #%d:" %s)
                    state_obj = d.state_list[s]
                    d.print_struc (state_obj, d.state_desc)
                    
                    if state_obj['trigger_index'] != 0xffffffff:
                        print("State trigger:")
                        script_obj = d.state_trigger_list[state_obj['trigger_index']]
                        d.print_script (script_obj)
                        
                        try:
                            print('Evals to:', self.eval_function (script_obj['code']))
                        except KeyError:
                            print("Unknown trigger")

                    j = 0
                    for transition in d.transition_list[state_obj['first_transition_index']:state_obj['first_transition_index']+state_obj['transition_cnt']]:
                        print('\n  Trans %d:' %j)
                        d.print_transition (transition)
                        print("\n")
                        j = j + 1
                    
                elif cmd == 'run':
                    # FIXME: optional arguments!
                    # FIXME: return to the last run dlg instead of the first one?
                    print("dlg reset")
                    step = False
                    values = {}
                    dialogs = {}
                    d = get_dialog (name)
                    state = 0
                    address = DLGDebugger.A_GET_STATE
                    
                elif cmd == 'trigger':
                    try:
                        print(eval_function (args))
                    except KeyError:
                        print("Unknown trigger:",  args)
                        
                elif cmd == 'continue':
                    step = False
                    break
                elif cmd == 'step':
                    step = True
                    break
                elif cmd == 'where':
                    print('DLG:',  d.name,  'state:',  state,  '@',  address)
                elif re.match ('\\d+',  cmd) and address == DLGDebugger.A_GET_REPLY:
                    address = DLGDebugger.A_TRANSITION
                    break
                else:
                    print('Unknown command:',  cmd)

                # TODO: execution history with 'undo' possibility

            if address == DLGDebugger.A_GET_STATE:
                state = get_next_state (d,  state)
                address = DLGDebugger.A_GET_REPLY
            
            if address == DLGDebugger.A_GET_REPLY:
                print_state (d,  d.state_list[state])
                
            if address == DLGDebugger.A_TRANSITION:
                next_dlg,  state = do_transition (d,  d.state_list[state],  int (cmd))
                address = DLGDebugger.A_GET_STATE
            
    
if __name__ == '__main__':
    infinity.builtins.load_game ("/home/benkovsk/dos/pst")
    dd = DLGDebugger()
    dd.run_dialog ("data/ABISHAB.DLG")
    #run_dialog ("DAnnah")

#else:
#    # FIXME: does not work
#    #__ALL__ = [ run_dialog ]

# End of file dlg_debugger.py
