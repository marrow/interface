# encoding: utf-8

"""Test the schema objects."""

from unittest import TestCase

from marrow.interface import Interface, schema

try:
    from collections import UserDict

except ImportError:
    from UserDict import UserDict



class TestInterface(TestCase):
    def test_interface_creation(self):
        class IUniversal(Interface):
            pass
        
        self.assertEquals(IUniversal.__attributes__, {})
    
    def test_interface_subclassing(self):
        class IGetter(Interface):
            __getitem__ = schema.Method(args=1)
        
        class IGetterSetter(IGetter):
            __setitem__ = schema.Method(args=2)
        
        self.assertEquals(IGetter.__attributes__, dict(
                __getitem__=IGetter.__getitem__)
            )
        
        self.assertEquals(IGetterSetter.__attributes__, dict(
                __getitem__ = IGetter.__getitem__,
                __setitem__ = IGetterSetter.__setitem__
            ))
    
    def test_bad_interface(self):
        with self.assertRaises(TypeError):
            class IBadInterface(Interface, object):
                pass
    
    def test_concrete_interface(self):
        with self.assertRaises(TypeError):
            class IConcrete(Interface):
                foo = 27
