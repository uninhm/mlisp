class Type:
    size = 0

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __str__(self):
        return self.__class__.__name__


class Pointer(Type):
    size = 8
    def __init__(self, typ=None):
        self.typ = typ

class Integer(Type):
    def __init__(self, signed, size):
        self.signed = signed
        self.size = size

class Character(Type):
    size = 1

def sizeof(typ): #TODO: remove
    return typ.size

def asm_size_repr(n):
    if n == 1:
        return 'byte'
    elif n == 2:
        return 'word'
    elif n == 4:
        return 'dword'
    elif n == 8:
        return 'qword'
    else:
        raise Exception('Unknown represetation for size: ' + str(n))

def str_to_type(s):
    if s == None:
        return None
    if s[0] in 'ui' and s[1:] in ('8', '16', '32', '64'):
        return Integer(s[0] == 'i', int(s[1:])//8)
    elif s == 'char':
        return Character()
    elif s == 'ptr':
        return Pointer()
    elif s.startswith('ptr-'):
        return Pointer(str_to_type(s[4:]))
    else:
        raise Exception("Unknown type class")
