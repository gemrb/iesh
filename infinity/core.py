# -*-python-*-
# iesh / ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2010 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

"""
Core and global definitions for the `infinity' package

"""

import os
import string
import sys

import defaults

global formats
formats = {}

global strrefs
strrefs = None

global keys
keys = None

global options
options = defaults.options

# Loaded IDS files
global ids
ids = {}

global bif_files
bif_files = {}

# These variables are filled after call to load_game()
game_dir = None
chitin_file = None
dialog_file = None
game_data_path = None

xor_key = "\x88\xa8\x8f\xba\x8a\xd3\xb9\xf5\xed\xb1\xcf\xea\xaa\xe4\xb5\xfb\xeb\x82\xf9\x90\xca\xc9\xb5\xe7\xdc\x8e\xb7\xac\xee\xf7\xe0\xca\x8e\xea\xca\x80\xce\xc5\xad\xb7\xc4\xd0\x84\x93\xd5\xf0\xeb\xc8\xb4\x9d\xcc\xaf\xa5\x95\xba\x99\x87\xd2\x9d\xe3\x91\xba\x90\xca"
"""Key used to `encrypt' some objects in IE files by XOR"""

global slash_trans
slash_trans = string.maketrans ('\\', '/')

t_cp1250 = '\xe1\xe8\xef\xe9\xec\xed\xf2\xf3\xf8\x9a\x9d\xfa\xf9\xfd\x9e\xc1\xc8\xcf\xc9\xcc\xcd\xd2\xd3\xd8\x8a\x8d\xda\xd9\xdd\x8e'
t_iso8859_2 = '\xe1\xe8\xef\xe9\xec\xed\xf2\xf3\xf8\xb9\xbb\xfa\xf9\xfd\xbe\xc1\xc8\xcf\xc9\xcc\xcd\xd2\xd3\xd8\xa9\xab\xda\xd9\xdd\xae'



global lang_trans
lang_trans = string.maketrans (t_cp1250, t_iso8859_2)

def translate_to_iso (s):
    return string.translate (s, lang_trans)

def cond (c, a, b):
    if c: return a
    else: return b

def translate_to_ord (s):
    return map (lambda c: (cond (ord (c) < 128, c, "\\x%02X" %(ord (c))), s))

#
# FIXME: this should be possibly refactored into its own file
#   with some controlling class.
# FIXME: also, it would be nice if it could be dynamically
#   created by format registrations, but that would leave out
#   unimplemented formats.
#
restype_list = [
    # type,    sig,     ext,  games, desc
    [ None,  'KEY ', 'KEY' ],
    [ None,  'BIFF', 'BIF' ],
    [ None,  'BIF ', 'CBF' ],
    [ None,  'TLK ', 'TLK' ],
    [ None,  None,   'ACM' ],
    [ None,  None,   'MUS' ],
    [ 0x001, 'BM',   'BMP' ],
    [ 0x002, None,   'MVE' ],
    [ 0x004, None,   'WAV' ],
    [ 0x004, 'WAVC', 'WAV' ],
    [ 0x004, 'WAVC', 'WAC' ],
    [ 0x005, 'WFX ', 'WFX' ], # no extension used, actually
    [ 0x006, 'PLT ', 'PLT' ],
    [ 0x3e8, 'BAM ', 'BAM' ],
    [ 0x3e8, 'BAMC', 'BAM' ],
    [ 0x3e9, 'WED ', 'WED' ],
    [ 0x3ea, 'CHUI', 'CHU' ],
    [ 0x3eb, None,   'TIS' ],
    [ 0x3ec, 'MOS ', 'MOS' ],
    [ 0x3ec, 'MOSC', 'MOS' ],
    [ 0x3ed, 'ITM ', 'ITM' ],
    [ 0x3ee, 'SPL ', 'SPL' ],
    [ 0x3ef, None,   'BCS' ],
    [ 0x3f0, None,   'IDS' ],
    [ 0x3f1, 'CRE ', 'CRE' ],
    [ 0x3f2, 'AREA', 'ARE' ],
    [ 0x3f3, 'DLG ', 'DLG' ],
    [ 0x3f4, '2DA',  '2DA' ],
    [ 0x3f5, 'GAME', 'GAM' ],
    [ None,  'SAV ', 'SAV' ],
    [ 0x3f6, 'STOR', 'STO' ],
    [ 0x3f7, 'WMAP', 'WMP' ],
    [ 0x3f8, 'CHR ', 'CHR' ],
    [ 0x3f8, 'EFF ', 'EFF' ],
    [ 0x3f9, None,   'BS' ],
    [ 0x3fa, 'CHR ', 'CHR' ],
    [ 0x3fb, 'VVC ', 'VVC' ],
    [ 0x3fc, '????', 'VEF' ],
    [ 0x3fd, 'PRO ', 'PRO' ],
    [ None,  None,   'RES' ],
    [ 0x3fe, None,   'BIO' ],
    [ 0x44c, None,   'BA' ],
    [ None,  None,   'BAF' ],
    [ 0x802, None,   'INI' ],
    [ 0x803, None,   'SRC' ],
    [ None,  'TLK ', 'TOH' ],
    [ None,  None,   'TOT' ],
    [ None,  None,   'VAR' ],
    ]

restype_hash = {}
restype_rev_hash = {}

def build_restype_tables (gametype = None):
    global restype_hash
    global restype_rev_hash

    restype_hash = {}
    restype_rev_hash = {}

    for restype in reversed (restype_list):
        # Add fields not set explicitly in restype_list
        if len (restype) < 5:
            restype.extend ([None] * (5 - len (restype)))

        if not restype[3]:
            restype[3] = set()

        if not restype[4]:
            restype[4] = set()

        type, sig, ext, games, desc = restype

        if type is not None and sig is not None:
            restype_hash[type] = sig.strip ()
            restype_rev_hash[sig.strip ()] = type




#restype_hash = {
#    0x0001 : 'BMP',
#    0x0002 : 'MVE',
#    0x0004 : 'WAV', # also WAVC
#    0x0005 : 'WFX',
#    0x0006 : 'PLT',
#    0x03e8 : 'BAM', # also BAMC
#    0x03e9 : 'WED',
#    0x03ea : 'CHUI',
#    0x03eb : 'TIS',
#    0x03ec : 'MOS', # also MOSC
#    0x03ed : 'ITM',
#    0x03ee : 'SPL',
#    0x03ef : 'BCS',
#    0x03f0 : 'IDS',
#    0x03f1 : 'CRE',
#    0x03f2 : 'ARE',
#    0x03f3 : 'DLG',
#    0x03f4 : '2DA',
#    0x03f5 : 'GAME',
#    0x03f6 : 'STOR',
#    0x03f7 : 'WMAP',
#    0x03f8 : 'CHR', # also  EFF
#    0x03f9 : 'BS',
#    0x03fa : 'CHR',
#    0x03fb : 'VVC',
#    0x03fc : 'VEF',
#    0x03fd : 'PRO',
#    0x03fe : 'BIO',
#    0x044c : 'BAH',
#    0x0802 : 'INI',
#    0x0803 : 'SRC',
#    }
#
#restype_rev_hash = {
#    '2DA'  : 0x03f4,
#    'ARE'  : 0x03f2,
#    'BAH'  : 0x044c,
#    'BAM'  : 0x03e8,
#    'BAMC' : 0x03e8,
#    'BCS'  : 0x03ef,
#    'BIO'  : 0x03fe,
#    'BMP'  : 0x0001,
#    'BS'   : 0x03f9,
#    'CHR'  : 0x03fa,
#    #'CHR' : 0x03f8,
#    'CHUI' : 0x03ea,
#    'CRE'  : 0x03f1,
#    'DLG'  : 0x03f3,
#    'EFF'  : 0x03f8,
#    'GAME' : 0x03f5,
#    'IDS'  : 0x03f0,
#    'INI'  : 0x0802,
#    'ITM'  : 0x03ed,
#    'MOS'  : 0x03ec,
#    'MOSC' : 0x03ec,
#    'MVE'  : 0x0002,
#    'PLT'  : 0x0006,
#    'PRO'  : 0x03fd,
#    'SPL'  : 0x03ee,
#    'SRC'  : 0x0803,
#    'STOR' : 0x03f6,
#    'TIS'  : 0x03eb,
#    'VEF'  : 0x03fc,
#    'VVC'  : 0x03fb,
#    'WAV'  : 0x0004,
#    'WAVC' : 0x0004,
#    'WED'  : 0x03e9,
#    'WFX'  : 0x0005,
#    'WMAP' : 0x03f7,
#    }

def find_res_type (**kw):
    """Return list of resource types matching the given parameters.

    Parameter can be type, sig, sig4, or ext. If more than one parameter is given, the
    result must satisfy each of them.
        type - numerical RESREF type
        sig - signature, trailing spaces are ignored
        sig4 - signature, trailing spaces must be exact
        ext - filename extension, leading dot is added automagically
        tag - 
        any -
    
    Example:
        find_res_type (sig='ITM')"""
        
    rtl = restype_list
    for key, value in kw.items ():
        if key == 'type':
            rtl = [ r for r in rtl if r[0] == value ]
        elif key == 'sig':
            value = "%-4s" %value
            rtl = [ r for r in rtl if r[1] == value ]
        elif key == 'sig4':
            rtl = [ r for r in rtl if r[1] == value ]
        elif key == 'ext' or key == 'name':
            value = value.upper ()
            if value.startswith ('.'):
                value = value[1:]
            rtl = [ r for r in rtl if r[2] == value ]
    
    return rtl


def type_to_ext (type):
    return [ r[2] for r in find_res_type (type=type) ]
    

#def sig_to_type (signature,  game_type = None):
#    pass

def register_format (signature, version, klass,  desc = None):
    """Register class `klass' for reading, parsing and (possibly) writing
    IE file format with given `signature' and `version'.  `desc' allows
    to specify text displayed in format list and should be used to 
    describe status/progress of implementation."""

    #core.formats[(signature, version)] = klass
    #formats[signature] = klass
    formats[(signature,  version)] = (klass,  desc)
    # FIXME: this is ugly temporary hack
    formats[(signature,  None)] = (klass,  desc)


def get_format (signature, version = None):
    try:
        return formats[(signature,  version)][0]
    except:
        return None


# FIXME: replace with find_res_type()
def get_format_by_type (type):
    try:
        signature = restype_hash[type]
        return get_format (signature)
    except:
        return None

def id_to_symbol (idsfile, id):
    # FIXME: ugly
    import traceback
    from stream import ResourceStream
    idsfile = idsfile.upper ()

    if not ids.has_key (idsfile):
        try:
            # FIXME: ugly & should use 'IDS' instead of 0x3F0
            idsobj = ResourceStream ().open (idsfile, 0x03F0).load_object ()
            #idsobj.read ()
            ids[idsfile] = idsobj
        except Exception, e:
            traceback.print_exc()
            print(e)
            return id

    try:
        return ids[idsfile].ids[id]
    except KeyError, e:
        sys.stderr.write ("Warning: No such id %d in %s\n" %(id, idsfile))
        return id
        
    #try:
    #    return core.ids[idsfile.upper ()].ids[id]
    #except:
    #    return None

def symbol_to_id (idsfile, sym):
    # FIXME: ugly
    import traceback
    from stream import ResourceStream
    idsfile = idsfile.upper ()

    if not ids.has_key (idsfile):
        try:
            # FIXME: ugly & should use 'IDS' instead of 0x3F0
            idsobj = ResourceStream ().open (idsfile, 0x03F0).load_object ()
            #idsobj.read ()
            ids[idsfile] = idsobj
        except Exception, e:
            traceback.print_exc()
            print e
            #return id
            return None

    try:
        return ids[idsfile].ids_re[sym]
    except KeyError, e:
        sys.stderr.write ("Warning: No such symbol %s in %s\n" %(sym, idsfile))
        #return sym
        return None
        

def find_file (filename, type = None):
    """Find file in the dirs specified in core.game_data_path and return its path.
    It tries exact filename match first and then case insensitive one."""

    # FIXME: use just normal match on case insensitive sysems (e.g. Windows)

    # FIXME: what about absolute filenames?
    
    # TODO: If filename has no extension, generate names with extensions allowed by a specified type
    #   (if no type is specified, maybe it could be acquired from keys.resref_hash?)
    #   Possibly try different extension even if one was specified, e.g. wav -> wavc, bif -> cbf

    # NOTE: it could cache os.listdir() results, but IMO it would be an overkill
    #   for probable use cases

    filename = filename.replace ('\\', '/')
    subdirs = filename.split (os.path.sep)  # FIXME: platform specific separator
    names = [ subdirs[-1] ]
    subdirs = subdirs[0:-1]

    try:
        dirs = game_data_path.split (os.path.pathsep) # FIXME: use list instead of string for path
    except AttributeError:
        dirs = [ '.' ]


    for dir in dirs:
        for subdir in subdirs:
            if os.path.exists (os.path.join (dir, subdir)):
                dir = os.path.join (dir, subdir)
                continue
            dirents = os.listdir (dir)
            matches = filter (lambda de: de.lower () == subdir.lower (), dirents)
            if matches:
                dir = os.path.join (dir, matches[0])
                continue
            else:
                dir = None
                break

        if dir is None:
            continue

        dirents = os.listdir (dir)
        for name in names:
            if os.access (os.path.join (dir,  name), os.F_OK):
                return os.path.join (dir,  name)
            matches = filter (lambda de: de.lower () == name.lower (), dirents)
            if matches:
                return os.path.join (dir,  matches[0])

    return None


def get_option (key):
    try:
        return options[key][0]
    except KeyError:
        raise RuntimeError ("Unknown option `%s'" %key)

def set_option (key,  value,  desc = None):
    try:
        opt = options[key]
        opt[0] = value
    except KeyError:
        # option does not exist yet, require desc and create it
        if desc is None:
            raise RuntimeError ("Unknown option `%s', `desc' required to create it" %key)
        options[key] = [value,  desc]


build_restype_tables ()

# End of file core.py
