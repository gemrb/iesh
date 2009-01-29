# -*-python-*-

dtypes = {}

class IE_Type:
    def __init__ (self):
        pass

    def repr (self, value, *args):
        return str (value)

    def read (self, stream, offset):
        return None

    def write (self, stream, offset, value):
        pass
    
    def size (self, value):
        return 0
        
class IE_WORD (IEType):
    def read (self, stream, offset):
        stream.read ()

class IE_STRING (IE_Type):
    pass

class IE_RESREF (IE_STRING):
    pass

# FIXME: read/write/ etc should be class methods, perhaps?

dtypes = {
    'STRING': IE_STRING (),
    'RESREF': IE_RESREF,
    }
