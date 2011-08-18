# encoding: utf-8

import UserDict

from marrow.interface import Interface
from marrow.interface.schema import Method


class IDictionary(Interface):
    __assume_interface__ = (dict, )
    
    __getitem__ = Method(args=1)
    __setitem__ = Method(args=2)
    __delitem__ = Method(args=1)


assert isinstance(dict, IDictionary)
assert isinstance(dict(), IDictionary)

assert isinstance(UserDict.UserDict, IDictionary)
assert isinstance(UserDict.UserDict(), IDictionary)
