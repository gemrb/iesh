#-*-python-*-
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

"""Built-in functions for the iesh shell. 

Functions which are ``built-into'' the iesh shell, meaning that this
module contents are automatically imported directly into iesh's 
namespace on startup."""

import os.path
import traceback

from infinity import core
from infinity.stream import ResourceStream, FileStream

###################################################
def load_game (game_dir, chitin_file = None, dialog_file = None):
    """Load key and dialog files from the 'game_dir' directory.

    The `game_dir' parameter is mandatory, the others are optional.
    Many commands assume that these two files are
    already loaded. The loaded objects are stored in core.keys and
    core.strrefs."""

    if chitin_file is None:
        chitin_file = core.get_option ('core.chitin_file')

    if dialog_file is None:
        dialog_file = core.get_option ('core.dialog_file')

    core.game_dir = game_dir
    core.game_data_path = game_dir
    core.chitin_file = chitin_file
    core.dialog_file = dialog_file
    
    # Load RESREF index file (CHITIN.KEY)
    chitin_file = core.find_file (chitin_file)
    stream = FileStream ().open (chitin_file)
    core.keys = core.get_format ('KEY') ()
    core.keys.read_header (stream)
    print "Loading %d file refs and %d RESREFs. This may take ages" %(core.keys.header['num_of_bifs'], core.keys.header['num_of_resrefs'])
    core.keys.read (stream)
    stream.close ()

    # LOAD STRREF index file (DIALOG.TLK)
    dialog_file = core.find_file (dialog_file)
    stream = FileStream ().open (dialog_file)
    core.strrefs = core.get_format ('TLK') ()
    core.strrefs.read_header (stream)
    print "Loading %d STRREFs. This may take eternity" %(core.strrefs.header['num_of_strrefs'])
    core.strrefs.read (stream)
    stream.close ()

###################################################
def load_object (name, type = None,  index = 0):
    """Load named object from a file located in filesystem or in game's data.

    Load file or resref `name'  and return Format object of appropriate type. 
    If `name' is not unique, specify resource type with `type' and eventually 
    `index' if there's still more than one."""

    try:
        stream = FileStream().open (name)
    except:
        stream = ResourceStream().open (name, type,  index)
    
    res = stream.load_object ()
    stream.close ()
    return res

###################################################
def print_object (name, type = None,  index = 0):
    """Load and print named object. See `load_object()' for details."""
    
    obj = load_object (name,  type,  index)
    obj.printme ()

###################################################
def export_object (name, filename, type = None, index = 0):
    """Export resource `name' into file `filename'. 

    If the `name' is not
    unique, specify resource type with `type' and eventually `index' if
    there's still more than one"""

    stream = ResourceStream ().open (name,  type,  index)
    fh = open (filename,  "w")
    fh.write (stream.buffer)
    fh.close ()
    stream.close ()
    
###################################################
def iterate_objects (fn, filter_fn = None, sort_fn = None, error_fn = None):
    """Execute function for each object of specified type."""
    
    # FIXME: this function opens and decodes a bif file EACH time some
    #   object from it is accessed, so it's slow as hell. It should use
    #   some caching

    #def resref_to_obj (res):
    #    print res['resref_name']
    #    return ResourceStream (res['resref_name'], type).load_object ()

    resrefs = []
    resrefs.extend (core.keys.resref_list)
    if callable (filter_fn):
        resrefs = filter (filter_fn, resrefs)
    
    if callable (sort_fn):
        resrefs.sort (sort_fn)

    for res in resrefs:
        print res['resref_name']
        obj = None

        if error_fn in ['msg', 'traceback'] or callable (error_fn):
            try:
                obj = ResourceStream ().open (res['resref_name'], res['type']).load_object ()
                fn (res, obj)
            except Exception, e:
                if callable (error_fn):
                    error_fn (res, obj, e)
                elif error_fn == 'msg':
                    print e
                elif error_fn == 'traceback':
                    traceback.print_exc ()
        else:
            obj = ResourceStream ().open (res['resref_name'], res['type']).load_object ()
            fn (res, obj)


###################################################
def iterate_objects_by_type (type, fn, filter_fn = None, sort_fn = None, error_fn = None):
    """Execute function for each object of specified type."""
    return iterate_objects (fn, filter_fn = lambda r: r['type'] == type, sort_fn = sort_fn, error_fn = error_fn)
    
###################################################
def find_str (regexp):
    """Find all strings in core.strrefs matching regular expression.
    
    Find all strings in loaded DIALOG.TLK file matching regular
    expression 'regexp' and prints the STRREFs and strings to stdout."""
    
    for o in core.strrefs.get_strref_by_str_re(regexp):
        print core.strrefs.strref_list.index(o), o['string']


###################################################
def sprintf (format_str, *params):
    return  format_str %(params)

def printf (format_str, *params):
    print sprintf (format_str, *params)


###################################################
def load_ids ():
    """Load (or try to) all IDS files."""

    def p (obj):
        obj.read ()
        print obj.stream.resref
        #obj.print_file ()
        
    iterate_objects_by_type (0x03f0, p)


###################################################
def print_restype_stats ():
    """Print list of RESREFs with count of objects of each type."""

    stats = {}
    
    for o in core.keys.resref_list:
        if not stats.has_key (o['type']):
            stats[o['type']] = 1
        else:
            stats[o['type']] = stats[o['type']] + 1

    for s in stats.keys ():
        if core.restype_hash.has_key (s):
            type = core.restype_hash[s]
        else:
            type = '??'
        print "0x%04x (%s):\t%5d" %(s, type, stats[s])

    return stats

###################################################
def print_formats ():
    """List recognized/implemented IE file formats"""
    
    flist = filter (lambda a: a[0][1] is not None,  core.formats.items ())
    flist.sort (lambda a,  b: 2 * cmp (a[0][0],  b[0][0]) + cmp (a[0][1],  b[0][1]))

    print "sign vers  class                 desc & status"
    print "-----------------------------------------------"
    for key,  value in flist:
        version = ''
        desc = ''
        if key[1] is not None:
            version = key[1]
        if value[1] is not None:
            desc = '- ' + value[1]
        klass_name = str (value[0])
        klass_name = klass_name.replace ('infinity.formats.',  '')
            
        print "%-4s %-4s  %-20s  %s" %(key[0],  version,  klass_name,  desc)


###################################################
def print_options (desc = True):
    """List known options with their values. If `desc' is True, list their descriptions as well."""

    options = core.options.items ()
    options.sort ()
    for key,  opt in options:
        if desc:
            print "%-30s - %s [%s]" %(key,  opt[1],  repr (opt[0]))
        else:
            print "%-30s - %s" %(key,  repr (opt[0]))

###################################################
# End of file builtins.py
