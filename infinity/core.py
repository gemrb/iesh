# -*-python-*-
# iesh / ie_shell.py - Simple shell for Infinity Engine-based game files
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

restype_list = [
    # type,    sig,     ext,  gametype, desc
    [ None,  'KEY ', '.key' ], 
    [ None,  'BIFF', '.bif' ], 
    [ None,  'BIF ', '.cbf' ], 
    [ None,  'TLK ', '.tlk' ], 
    [ None,  None,   '.acm' ], 
    [ None,  None,   '.mus' ], 
    [ 0x001, None,   '.bmp' ],
    [ 0x002, None,   '.mve' ],
    [ 0x004, None,   '.wav' ],
    [ 0x004, 'WAVC', '.wav' ],
    [ 0x004, 'WAVC', '.wac' ],
    [ 0x005, 'WFX ', None ],
    [ 0x006, 'PLT ', '.plt' ],
    [ 0x3e8, 'BAM ', '.bam' ],
    [ 0x3e8, 'BAMC', '.bam' ],
    [ 0x3e9, 'WED ', '.wed' ],
    [ 0x3ea, 'CHUI', '.chu' ],
    [ 0x3eb, None,   '.tis' ],
    [ 0x3ec, 'MOS ', '.mos' ],
    [ 0x3ec, 'MOSC', '.mos' ],
    [ 0x3ed, 'ITM ', '.itm' ],
    [ 0x3ee, 'SPL ', '.spl' ],
    [ 0x3ef, None,   '.bcs' ],
    [ 0x3f0, None,   '.ids' ],
    [ 0x3f1, 'CRE ', '.cre' ],
    [ 0x3f2, 'AREA', '.are' ],
    [ 0x3f3, 'DLG ', '.dlg' ],
    [ 0x3f4, '2DA',  '.2da' ],
    [ 0x3f5, 'GAME', '.gam' ],
    [ None,  'SAV ', '.sav' ],
    [ 0x3f6, 'STOR', '.sto' ],
    [ 0x3f7, 'WMAP', '.wmp' ],
    [ 0x3f8, 'CHR ', '.chr' ],
    [ 0x3f8, 'EFF ', '.eff' ],
    [ 0x3f9, None,   '.bs' ],
    [ 0x3fa, 'CHR ', '.chr' ],
    [ 0x3fb, 'VVC ', '.vvc' ],
    [ 0x3fc, '????', '.vef' ],
    [ 0x3fd, 'PRO ', '.pro' ],
    [ None,  None,   '.res' ],
    [ 0x3fe, None,   '.bio' ],
    [ 0x44c, None,   '.ba' ],
    [ None,  None,   '.baf' ],
    [ 0x802, None,   '.ini' ],
    [ 0x803, None,   '.src' ],
    [ None,  'TLK ', '.toh' ],
    [ None,  None,   '.tot' ],
    [ None,  None,   '.var' ],
    ]

restype_hash = {
    0x0001 : 'BMP',
    0x0002 : 'MVE',
    0x0004 : 'WAV', # also WAVC
    0x0005 : 'WFX',
    0x0006 : 'PLT',
    0x03e8 : 'BAM', # also BAMC
    0x03e9 : 'WED',
    0x03ea : 'CHUI',
    0x03eb : 'TIS',
    0x03ec : 'MOS', # also MOSC
    0x03ed : 'ITM',
    0x03ee : 'SPL',
    0x03ef : 'BCS',
    0x03f0 : 'IDS',
    0x03f1 : 'CRE',
    0x03f2 : 'ARE',
    0x03f3 : 'DLG',
    0x03f4 : '2DA',
    0x03f5 : 'GAME',
    0x03f6 : 'STOR',
    0x03f7 : 'WMAP',
    0x03f8 : 'CHR', # also  EFF
    0x03f9 : 'BS',
    0x03fa : 'CHR',
    0x03fb : 'VVC',
    0x03fc : 'VEF',
    0x03fd : 'PRO',
    0x03fe : 'BIO',
    0x044c : 'BAH',
    0x0802 : 'INI',
    0x0803 : 'SRC',
    }

restype_rev_hash = {
    '2DA'  : 0x03f4,
    'ARE'  : 0x03f2,
    'BAH'  : 0x044c,
    'BAM'  : 0x03e8,
    'BAMC' : 0x03e8,
    'BCS'  : 0x03ef,
    'BIO'  : 0x03fe,
    'BMP'  : 0x0001,
    'BS'   : 0x03f9,
    'CHR'  : 0x03fa,
    #'CHR' : 0x03f8,
    'CHUI' : 0x03ea,
    'CRE'  : 0x03f1,
    'DLG'  : 0x03f3,
    'EFF'  : 0x03f8,
    'GAME' : 0x03f5,
    'IDS'  : 0x03f0,
    'INI'  : 0x0802,
    'ITM'  : 0x03ed,
    'MOS'  : 0x03ec,
    'MOSC' : 0x03ec,
    'MVE'  : 0x0002,
    'PLT'  : 0x0006,
    'PRO'  : 0x03fd,
    'SPL'  : 0x03ee,
    'SRC'  : 0x0803,
    'STOR' : 0x03f6,
    'TIS'  : 0x03eb,
    'VEF'  : 0x03fc,
    'VVC'  : 0x03fb,
    'WAV'  : 0x0004,
    'WAVC' : 0x0004,
    'WED'  : 0x03e9,
    'WFX'  : 0x0005,
    'WMAP' : 0x03f7,
    }

def find_res_type (type, sig = None, ext = None):
    rtl = restype_list
    if type is not None:
        rtl = [ r for r in rtl if r[0] == type ]
    if sig is not None:
        rtl = [ r for r in rtl if r[1] == sig ]
    if ext is not None:
        sig = sig.lower ()
        if not sig.startswith ('.'):
            sig = '.' + sig
        rtl = [ r for r in rtl if r[2] == sig ]
    
    return rtl


def type_to_ext (type):
    return [ r[2] for r in find_res_type (type) ]
    

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
            print e
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
    

def find_file (filename):
    dirs = game_data_path.split (':')
    for dir in dirs:
        if os.access (os.path.join (dir,  filename), os.F_OK):
            return os.path.join (dir,  filename)
    
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


# End of file core.py
