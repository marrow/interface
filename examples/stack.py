# encoding: utf-8


from marrow.interface.core import Interface
from marrow.interface.declaration import Method


class IStack(Interface):
    __len__ = Method(args=0)
    push = Method(args=1, names=('value', ))
    pop = Method(args=0)
    peek = Method(args=0)


class Stack(object):
    def __init__(self, iv=None):
        self.data = list(iv) if iv else list()
    
    def push(self, value):
        self.data.append(value)
        return value
    
    def pop(self):
        return self.data.pop()
    
    def peek(self):
        return self.data[-1]
    
    def __len__(self):
        return len(self.data)


assert isinstance(Stack(), IStack)
assert isinstance(Stack, IStack)
