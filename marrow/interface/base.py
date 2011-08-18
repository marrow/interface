# encoding: utf-8

from marrow.interface import Interface
from marrow.interface.schema import *


__all__ = ['IMapping']



class IMapping(Interface):
    __assume_interface__ = (dict,)
    __getitem__ = Method(args=1)
    __setitem__ = Method(args=2)
    __delitem__ = Method(args=1)
