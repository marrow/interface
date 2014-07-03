# encoding: utf-8

from marrow.interface import Interface
from marrow.interface.schema import Method

try:
    from collections import UserDict

except ImportError:
    from UserDict import UserDict


__all__ = ['IDictionary']


class IDictionary(Interface):
    __assume_interface__ = (dict, )
    
    __getitem__ = Method(args=1)
    __setitem__ = Method(args=2)
    __delitem__ = Method(args=1)


assert isinstance(dict, IDictionary)
assert isinstance(dict(), IDictionary)

assert isinstance(UserDict, IDictionary)
assert isinstance(UserDict(), IDictionary)
