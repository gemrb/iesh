#-*-python-*-

from formats import *

# print buttons which have frame indices other than 0, 1, 0, 0
def print_button_frames (filename):
    c = chui.CHUI_Format (filename)
    c.decode_file()


    for w in c.window_list:
        for b in w['control_list']:
            if b['type'] != 0: continue

            if (0, 1, 0, 0) != (b['frame_unpressed'], b['frame_pressed'], b['frame_selected'], b['frame_disabled']):
                mark = "<---"
            else:
                mark = ""
            
            print "%2d/%2d: %d %d %d %d" %(w['id'], b['id'], b['frame_unpressed'], b['frame_pressed'], b['frame_selected'], b['frame_disabled']), mark
