from marrow.interface import Interface
from marrow.interface.schema import Method

class ILengthly(Interface):
    __len__ = Method(args=0)

class MetaLengthly(type):
    def __len__(self): return 0

class MyLengthly(object):
    __metaclass__ = MetaLengthly

assert len(MyLengthly) == 0
assert isinstance(MyLengthly, ILengthly) is True

# len(MyLengthly()) == 0 # nope, error
assert isinstance(MyLengthly(), ILengthly) is False

# Note that the above is _correct_.  You _can't_ len() instances.
