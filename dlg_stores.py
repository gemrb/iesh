#!/usr/bin/env python

"""Create DLG file that has different shops as conversation nodes,
for quick access to different shops when debugging stores in the original pst"""

import os.path

from infinity import core
from infinity.stream import FileStream
from infinity.formats import dlg
from infinity.builtins import load_game, load_object, restore_state


def main ():

    # this file is created with infinity.builtins.save_state()
    restore_state(os.path.expanduser('~/.iesh_restore-pst'))


    d = dlg.DLG_Format()
    d.header = {}
    d.header['signature'] = 'DLG '
    d.header['version'] = 'V1.0'

    start = {
        'npc_text': 50533,
        'first_transition_index': 0,
        'transition_cnt': 0,
        'trigger_index': 0,
        }

    trigger = {
        'code': "true;",
        }

    d.state_list.append(start)
    d.state_trigger_list.append(trigger)


    #resrefs = ('ALEKSTR', 'BARSE', 'COAX', 'EMORIC', 'FELL', 'FHJULL', 'VRIS', )
    resrefs = [ r['resref_name']  for r in core.keys.get_resref_by_type(0x3f6) ]


    for i, resref in enumerate(resrefs):
        store = load_object(resref, type=0x3f6)

        store.print_header()

        name = store.header['name']
        if name == 0xffffffff:
            name = 50534

        transition = {
            'flags': 0x0d,
            'pc_text': name,
            'journal_text': 0,
            'trigger_index': 0xffffffff,
            'action_index': i,
            'next_dialog': '',
            'next_state': 0,
            }

        action = {
            'code': "StartStore(\"%s\",Protagonist)" %resref,
            }

        d.transition_list.append(transition)
        d.action_list.append(action)
        start['transition_cnt'] += 1


    f = FileStream().open("test.dlg", "w")
    d.write(f)
    f.close()


if __name__ == '__main__':
    main()
