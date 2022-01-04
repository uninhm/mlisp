class Type:
    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __str__(self):
        return self.__class__.__name__


class Pointer(Type):
    size = 8
    def __init__(self, typ=None):
        self.typ = typ

class Integer(Type):
    size = 8

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
