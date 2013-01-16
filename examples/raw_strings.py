#-*-python-*-

#import os.path

from plugins import core

###################################################
# Print hexa code of characters in given strref,
#   without conversion

def print_raw_str (strref):
    print(core.strrefs.strref_list[strref]['string_raw'])
    print([c + " (%02x)" %ord (c) for c in core.strrefs.strref_list[strref]['string_raw']])

