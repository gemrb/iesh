# -*-python-*-

import string


global formats
formats = {}

global strrefs
strrefs = None

global keys
keys = None

game_dir = None
chitin_file = 'CHITIN.KEY'
dialog_file = 'dialog.tlk'

global slash_trans
slash_trans = string.maketrans ('\\', '/')

t_cp1250 = 'áèïéìíòóøšúùıÁÈÏÉÌÍÒÓØŠÚÙİ'
t_iso8859_2 = 'áèïéìíòóø¹»úùı¾ÁÈÏÉÌÍÒÓØ©«ÚÙİ®'

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


def register_format (signature, version, klass):
    #core.formats[(signature, version)] = klass
    formats[signature] = klass


def get_format (signature, version = None):
    try:
        return formats[signature]
    except:
        return None

