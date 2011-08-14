# encoding: utf-8

import UserDict

from marrow.interface.core import Interface
from marrow.interface.declaration import Method


class IDictionary(Interface):
    __getitem__ = Method(args=1)
    __setitem__ = Method(args=0)
    __delitem__ = Method(args=1)


assert isinstance(UserDict.UserDict(), IDictionary)
