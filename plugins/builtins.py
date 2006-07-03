#-*-python-*-

import os.path

from plugins import core
from formats.stream import ResourceStream, FileStream

###################################################
def load_game (game_dir, chitin_file = core.chitin_file, dialog_file = core.dialog_file):
    """Loads key and dialog files from the specified directory.
    The directory parameter is mandatory, the others are optional.
    Most of the other commands assume that these two files are
    already loaded. The loaded objects are stored in core.keys and
    core.strrefs."""

    core.game_dir = game_dir
    core.chitin_file = chitin_file
    core.dialog_file = dialog_file
    
    # Load RESREF index file (CHITIN.KEY)
    core.keys = core.get_format ('KEY') (os.path.join (game_dir, chitin_file))
    core.keys.decode_header ()
    print "Loading %d file refs and %d RESREFs. This may take ages" %(core.keys.header['num_of_bifs'], core.keys.header['num_of_resrefs'])
    core.keys.decode_file ()


    # LOAD STRREF index file (DIALOG.TLK)
    core.strrefs = core.get_format ('TLK') (os.path.join (game_dir, dialog_file))
    core.strrefs.decode_header ()
    print "Loading %d STRREFs. This may take eternity" %(core.strrefs.header['num_of_strrefs'])
    core.strrefs.decode_file ()


###################################################
def load_object (name):

    try:
        fh = open (name)
    except:
        fh = None

    if fh:
        fh.close ()
        return FileStream(name).load_object ()
    else:
        return ResourceStream(name).load_object ()

    
###################################################
def find_str (text):
    """Finds all strings in loaded DIALOG.TLK file matching regular expression
    and prints their STRREFs"""
    
    for o in core.strrefs.get_strref_by_str_re(text):
        print core.strrefs.strref_list.index(o), o['string']

###################################################
def export_obj (name, filename, type = 0):
    """Exports resource `name' into file `filename'. If the `name' is not
    unique, specify resource type with `type'"""
    
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


###################################################
def iterate_objects_by_type (type, fn):

    # FIXME: this function opens and decodes a bif file EACH time some
    #   object from it is accessed, so it's slow as hell. It should use
    #   some caching

    #def resref_to_obj (res):
    #    print res['resref_name']
    #    return ResourceStream (res['resref_name'], type).load_object ()

    for res in filter (lambda res: res['type'] == type, core.keys.resref_list):
        print res['resref_name']
        obj = ResourceStream (res['resref_name'], type).load_object ()
        fn (obj)
    

###################################################
def sprintf (format_str, params):
    return  format_str %(params)

def printf (format_str, params):
    print sprintf (format_str, params)

def loaded_object (obj):
    obj.decode_file ()
    return obj

###################################################
def pok():
    def p (obj):
        obj.decode_file ()
        obj.print_file ()

    iterate_objects_by_type (0x03ed, p)

###################################################
def load_ids (name):
    def p (obj):
        obj.decode_file ()
        print obj.stream.resref
        #obj.print_file ()
        
    iterate_objects_by_type (0x03f0, p)

###################################################
def get_restype_stats ():
    stats = {}
    for o in core.keys.resref_list:
        if not stats.has_key (o['type']):
            stats[o['type']] = 1
        else:
            stats[o['type']] = stats[o['type']] + 1

    return stats

        
###################################################
def print_restype_stats ():
    stats = get_restype_stats ()
    for s in stats.keys ():
        if core.restype_hash.has_key (s):
            type = core.restype_hash[s]
        else:
            type = '??'
        print "0x%04x (%s):\t%5d" %(s, type, stats[s])


###################################################
# End of file builtins.py
