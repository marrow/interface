# encoding: utf-8

"""Test the schema objects."""

from marrow.interface import Interface, schema


class MockAttribute(schema.Attribute):
	def __init__(self, *args, **kw):
		super(MockAttribute, self).__init__(*args, **kw)
		self.called = False
	
	def __call__(self, inst):
		self.called = True
		return hasattr(inst,self.__name__)


class TestInterface:
	def test_interface_creation(self):
		class IUniversal(Interface):
			pass
		
		assert IUniversal.__attributes__ == {}
	
	def test_interface_subclassing(self):
		class IGetter(Interface):
			__getitem__ = schema.Method(args=1)
		
		class IGetterSetter(IGetter):
			__setitem__ = schema.Method(args=2)
		
		assert IGetter.__attributes__ == dict(
				__getitem__=IGetter.__getitem__
			)
		
		assert IGetterSetter.__attributes__ == dict(
				__getitem__ = IGetter.__getitem__,
				__setitem__ = IGetterSetter.__setitem__
			)
	
	def test_bad_interface(self):
		try:
			class IBadInterface(Interface, object):
				pass
		except TypeError:
			pass
	
	def test_concrete_interface(self):
		try:
			class IConcrete(Interface):
				foo = 27
		except TypeError:
			pass
	
	def test_check(self):
		class IRig(Interface):
			mock = MockAttribute()
		
		assert not IRig.mock.called
		assert isinstance(IRig, IRig)
		assert IRig.mock.called
		assert not isinstance(object(), IRig)
	
	def test_assumption(self):
		class IDict(Interface):
			__assume__ = (dict, )
		
		assert isinstance(dict, IDict)
		assert isinstance(dict(), IDict)
