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

import cPickle
import os.path
import sys
import traceback

from infinity import core
from infinity.stream import ResourceStream, FileStream, OverrideStream

###################################################
def load_game (game_dir, chitin_file = None, dialog_file = None):
    """Load key and dialog files from the 'game_dir' directory.

    The `game_dir' parameter is mandatory, the others are optional.
    Many commands assume that these two files are
    already loaded. The loaded objects are stored in core.keys, core.override
    and core.strrefs."""

    if chitin_file is None:
        chitin_file = core.get_option ('core.chitin_file')

    if dialog_file is None:
        dialog_file = core.get_option ('core.dialog_file')

    core.game_dir = game_dir
    core.game_data_path = game_dir
    core.override_dir = core.locate_override ()
    core.chitin_file = chitin_file
    core.dialog_file = dialog_file

    # Load data from the override
    if core.override_dir is not None:
        core.override = core.load_override ()

    # Load RESREF index file (CHITIN.KEY)
    chitin_file = core.find_file (chitin_file)
    stream = FileStream ().open (chitin_file)
    core.keys = stream.get_format () ()
    core.keys.read_header (stream)
    print("Loading %d file refs and %d RESREFs. This may take ages" %(core.keys.header['num_of_bifs'], core.keys.header['num_of_resrefs']))
    core.keys.read (stream)
    stream.close ()

    # LOAD STRREF index file (DIALOG.TLK)
    dialog_file = core.find_file (dialog_file)
    stream = FileStream ().open (dialog_file)
    core.strrefs = stream.get_format () ()
    core.strrefs.read_header (stream)
    print("Loading %d STRREFs. This may take eternity" %(core.strrefs.header['num_of_strrefs']))
    core.strrefs.read (stream)
    stream.close ()

###################################################
def save_state (filename):
    """Saves some core variables (especially keys and strrefs), so that they
    can be later loaded faster than from IE data files."""
    data = [core.game_dir, core.override, core.override_dir, core.chitin_file,
            core.dialog_file, core.keys, core.strrefs, core.game_data_path ]
    fh = open (filename,  'w')
    cPickle.dump (data,  fh)
    fh.close ()

###################################################
def restore_state (filename):
    """Loads some core variables (especially keys and strrefs) saved
    by save_state() function, much faster than from IE data files."""
    fh = open (filename)
    data = cPickle.load (fh)
    fh.close ()
    # old format from before override dir support
    if len(data) == 6:
        core.game_dir, core.chitin_file, core.dialog_file, core.keys, core.strrefs, core.game_data_path = data
        core.override_dir = core.locate_override ()
        if core.override_dir is not None:
            core.override = core.load_override ()
    else:
        core.game_dir, core.override, core.override_dir, core.chitin_file, core.dialog_file, core.keys, core.strrefs, core.game_data_path = data

###################################################
def find_objects (name, filetype = None):
    """Look up named objects in game's data or in the override directory."""

    filetype = core.ext_to_type(filetype)
    override_obj = core.search_override (name, filetype)
    resref_obj = core.keys.get_resref_by_name (name)

    if filetype is not None:
        resref_obj = filter (lambda o: o['type'] == filetype, resref_obj)

    if override_obj:
        print ("Override:")
        for o in override_obj:
            print (
                "  File: %s, Type: %s, location: %s"
                %(o['resref_name'], core.type_to_ext(o['type'])[0], o['path'])
            )
    else:
        print "Nothing found in override!"

    if resref_obj:
        print ("Game data:")
        for o in resref_obj:
            print (
                "  File: %s, Type: %s, location: %s"
                %(o['resref_name'], core.type_to_ext(o['type'])[0], o['file_name']['file_name'])
            )
    else:
        print "Nothing found in game data!"

###################################################
def load_object (name, type = None, index = 0, ignore_override = False):
    """Load named object from a file located in filesystem or in game's data.

    Load file or resref `name' and return Format object of appropriate type.
    If `name' is not unique, specify resource type with `type' and eventually
    `index' if there's still more than one.

    If you want to avoid the override folder, specify the appropriate value for
    `ignore_override' parameter."""

    stream = None

    if not ignore_override:
        try:
            stream = OverrideStream().open (name, type, index)
        except RuntimeError as e:
            print sys.exc_info()[1]

        try:
            stream = stream or FileStream().open (name)
        except:
            print "File not found on filesystem, checking BIF files"

    if stream is None or ignore_override:
        try:
            stream = ResourceStream().open (name, type, index)
        except:
            print sys.exc_info()[1]
            return None

    res = stream.load_object ()
    stream.close ()
    return res

###################################################
def print_object (name, type = None,  index = 0):
    """Load and print named object. See `load_object()' for details."""

    obj = load_object (name,  type,  index)
    obj.printme ()

###################################################
def export_object (name, filename, type = None, index = 0, ignore_override=False):
    """Export resource `name' into file `filename'.

    If the `name' is not unique, specify resource type with `type' and eventually
    `index' if there's still more than one.

    Specify `ignore_override' if you want to export straight from the game's data."""

    stream = None

    if not ignore_override:
        try:
            stream = OverrideStream ().open (name, type, index)
        except:
            pass

    if stream is None or ignore_override:
        stream = ResourceStream ().open (name, type, index)

    fh = open (filename, "w")
    fh.write (stream.buffer)
    fh.close ()
    stream.close ()


###################################################
class ObjectIterator:
    """Iterate over specified resrefs, load them as objects and generate pairs (resref, object).

    Parameters:

    type=[num|name] - select resrefs specified by type id or type name
    filter - ref to function taking resref as a parameter and returning True for
             resrefs which should be selected
    sort - fiels name to sort on or ref to function which compares two resrefs
    error=[ignore|msg|traceback|throw|<fn>] - how to handle errors during a loading of a resref
    names=all - print resref names as they are loaded."""

    # FIXME: this function opens and decodes a bif file EACH time some
    #   object from it is accessed, unless you set 'use_cache' option

    # FIXME: add names=ok|error, eventually ok2, error2 to specidy when to
    #   print the label

    def __init__ (self, **kw):
        self.resrefs = core.keys.resref_list[:]

        if 'type' in kw and type (kw['type']) == type (1):
            self.resrefs = filter (lambda r, t=kw['type']: r['type'] == t, self.resrefs)
        elif 'type' in kw:
            tid = core.find_res_type (name=kw['type'])[0][0]
            self.resrefs = filter (lambda r, t=tid: r['type'] == t, self.resrefs)

        if 'filter' in kw and callable (kw['filter']):
            self.resrefs = filter (kw['filter'], self.resrefs)

        if 'sort' in kw and callable (kw['sort']):
            self.resrefs.sort (kw['sort'])

        if 'error' in kw:
            self.error_fn = kw['error']
        else:
            self.error_fn = None

        if 'names' in kw:
            self.print_names = kw['names']
        else:
            self.print_names = 'all'


    def __iter__ (self):
        return self


    def next (self):
        if not self.resrefs:
            raise StopIteration

        res = self.resrefs.pop (0)

        if self.print_names == 'all':
            print(res['resref_name'])

        obj = None

        #if error_fn in ['msg', 'traceback', 'ignore'] or callable (error_fn):
        try:
            obj = ResourceStream ().open (res['resref_name'], res['type']).load_object ()
            #fn (res, obj)
        except Exception, e:
            if callable (self.error_fn):
                self.error_fn (res, obj, e)
            elif self.error_fn == 'msg':
                for msg in traceback.format_exception_only (sys.exc_type, sys.exc_value):
                    print msg
            elif self.error_fn == 'traceback':
                traceback.print_exc ()
            elif self.error_fn == 'ignore':
                pass
            else:
                #traceback.print_exc ()
               raise

        return res, obj


###################################################
def find_str (regexp):
    """Find all strings in core.strrefs matching regular expression.

    Find all strings in loaded DIALOG.TLK file matching regular
    expression 'regexp' and prints the STRREFs and strings to stdout."""

    for o in core.strrefs.get_strref_by_str_re(regexp):
        print(core.strrefs.strref_list.index(o), o['string'])


###################################################
def sprintf (format_str, *params):
    return  format_str %(params)

def printf (format_str, *params):
    print(sprintf (format_str, *params))


###################################################
def load_ids ():
    """Load (or try to) all IDS files."""

    def p (obj):
        obj.read ()
        print(obj.stream.resref)
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
        print("0x%04x (%s):\t%5d" %(s, type, stats[s]))

    return stats

###################################################
def print_formats ():
    """List recognized/implemented IE file formats"""

    flist = filter (lambda a: a[1] is not None,  core.fmt_signatures.items ())
    flist.sort (lambda a, b: cmp (a[0], b[0]))

    print("signature    class")
    print("----------|------------------------")
    for sig, klass in flist:
        klass_name = str (klass[0]).split("'")
        klass_name = klass_name[1].replace ('infinity.formats.',  '')
        sig = sig.replace('\n', ' ').replace('\r', ' ').rstrip()
        if len(sig) > 1:
            print("%-10s|  %s" %(sig, klass_name))


###################################################
def print_options (desc = True):
    """List known options with their values. If `desc' is True, list their descriptions as well."""

    options = core.options.items ()
    options.sort ()
    for key,  opt in options:
        if desc:
            print("%-30s - %s [%s]" %(key,  opt[1],  repr (opt[0])))
        else:
            print("%-30s - %s" %(key,  repr (opt[0])))

###################################################
# End of file builtins.py
