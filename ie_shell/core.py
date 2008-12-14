# -*-python-*-

import string


global formats
formats = {}

global strrefs
strrefs = None

global keys
keys = None

global options
options = {}

# Loaded IDS files
global ids
ids = {}

game_dir = None
chitin_file = 'CHITIN.KEY'
dialog_file = 'dialog.tlk'

xor_key = "\x88\xa8\x8f\xba\x8a\xd3\xb9\xf5\xed\xb1\xcf\xea\xaa\xe4\xb5\xfb\xeb\x82\xf9\x90\xca\xc9\xb5\xe7\xdc\x8e\xb7\xac\xee\xf7\xe0\xca\x8e\xea\xca\x80\xce\xc5\xad\xb7\xc4\xd0\x84\x93\xd5\xf0\xeb\xc8\xb4\x9d\xcc\xaf\xa5\x95\xba\x99\x87\xd2\x9d\xe3\x91\xba\x90\xca"


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
    [0x0001, 'BMP', ''],
    [0x0002, 'MVE', ''],
    [0x0004, 'WAV', ''],
    [0x0004, 'WAVC', ''],
    [0x0005, 'WFX', ''],
    [0x0006, 'PLT', ''],
    [0x03e8, 'BAM', ''],
    [0x03e8, 'BAMC', ''],
    [0x03e9, 'WED', ''],
    [0x03ea, 'CHUI', ''],
    [0x03eb, 'TIS', ''],
    [0x03ec, 'MOS', ''],
    [0x03ec, 'MOSC', ''],
    [0x03ed, 'ITM', ''],
    [0x03ee, 'SPL', ''],
    [0x03ef, 'BCS', ''],
    [0x03f0, 'IDS', ''],
    [0x03f1, 'CRE', ''],
    [0x03f2, 'ARE', ''],
    [0x03f3, 'DLG', ''],
    [0x03f4, '2DA', ''],
    [0x03f5, 'GAME', ''],
    [0x03f6, 'STOR', ''],
    [0x03f7, 'WMAP', ''],
    [0x03f8, 'CHR', ''],
    [0x03f8, 'EFF', ''],
    [0x03f9, 'BS', ''],
    [0x03fa, 'CHR', ''],
    [0x03fb, 'VVC', ''],
    [0x03fc, 'VEF', ''],
    [0x03fd, 'PRO', ''],
    [0x03fe, 'BIO', ''],
    [0x044c, 'BAH', ''],
    [0x0802, 'INI', ''],
    [0x0803, 'SRC', ''],
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


def register_format (signature, version, klass):
    #core.formats[(signature, version)] = klass
    formats[signature] = klass


def get_format (signature, version = None):
    try:
        return formats[signature]
    except:
        return None


def get_format_by_type (type):
    try:
        signature = restype_hash[type]
        return get_format (signature)
    except:
        return None

