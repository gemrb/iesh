#-*-python-*-

import os.path

from plugins import core

###################################################
# Find all strings in loaded DIALOG.TLK file matching regular expression
#    and print their STRREFs
def find_str (text):
    for o in core.strrefs.get_strref_by_str_re(text):
        print core.strrefs.strref_list.index(o), o['string']

# Export resource `name' into file `filename'. If the `name' is not unique
#   specify resource type with `type'
def export_obj (name, filename, type = 0):
     oo = core.keys.get_resref_by_name_re(name)
     if type != 0:
         oo = filter (lambda o: o['type'] == type, oo)

     if len (oo) > 1 and type == 0:
         print "More than one result"
         return

     o = oo[0]
     
     src_file = core.keys.bif_list[o['locator_src_ndx']]
     b = core.formats['BIFF'] (os.path.join (core.game_dir, src_file['file_name']))
     b.decode_file ()
     b.save_file_res (filename, b.file_list[o['locator_ntset_ndx']])



def load_ids (name):
    export_obj (name, "data/tmpobj.tmp", 0x03f0)
    pass

def get_format_for_obj (stream):
    from types import StringType, FileType

    if type (stream) is FileType:
        old_pos = stream.tell ()
        stream.seek (0)
        signature = stream.read (4)
        stream.seek (old_pos)

        print signature

    elif type (stream) is StringType:
        fh = open (stream)
        res = get_format_for_obj (fh)
        fh.close ()
        return res

def get_restype_stats ():
    stats = {}
    for o in core.keys.resref_list:
        if not stats.has_key (o['type']):
            stats[o['type']] = 1
        else:
            stats[o['type']] = stats[o['type']] + 1

    return stats

        
def print_restype_stats ():
    stats = get_restype_stats ()
    for s in stats.keys ():
        if core.restype_hash.has_key (s):
            type = core.restype_hash[s]
        else:
            type = '??'
        print "0x%04x (%s):\t%5d" %(s, type, stats[s])
