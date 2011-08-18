# encoding: utf-8

import UserDict

from marrow.interface import Interface
from marrow.interface.schema import Method


class IDictionary(Interface):
    __getitem__ = Method(args=1)
    __setitem__ = Method(args=0)
    __delitem__ = Method(args=1)


assert isinstance(UserDict.UserDict(), IDictionary)
