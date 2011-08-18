# encoding: utf-8

"""Test the schema objects."""

from unittest import TestCase
from UserDict import UserDict

from marrow.interface import Interface, schema



class TestInterface(TestCase):
    def test_interface_creation(self):
        class IUniversal(Interface):
            pass
        
        self.assertEquals(IUniversal.__abstract__, {})
    
    def test_interface_subclassing(self):
        class IGetter(Interface):
            __getitem__ = schema.Method(args=1)
        
        class IGetterSetter(IGetter):
            __setitem__ = schema.Method(args=2)
        
        self.assertEquals(IGetter.__abstract__, dict(
                __getitem__=IGetter.__getitem__)
            )
        
        self.assertEquals(IGetterSetter.__abstract__, dict(
                __getitem__ = IGetter.__getitem__,
                __setitem__ = IGetterSetter.__setitem__
            ))
    
    def test_bad_interface(self):
        with self.assertRaises(TypeError):
            class IBadInterface(Interface, object):
                pass
    
    def test_conflicting_interfaces(self):
        class IGetter(Interface):
            __getitem__ = schema.Method(args=1)
        
        with self.assertRaises(TypeError):
            class IGetterSetter(IGetter):
                __getitem__ = schema.Method(args=2)
                __setitem__ = schema.Method(args=2)
    
    def test_concrete_interface(self):
        with self.assertRaises(TypeError):
            class IConcrete(Interface):
                foo = 27


class TestExampleInterface(TestCase):
    def setUp(self):
        class IDictlike(Interface):
            __assume_interface__ = (dict, )
            __getitem__ = schema.Method(args=1)
            __setitem__ = schema.Method(args=2)
            __delitem__ = schema.Method(args=1)
        
        self.interface = IDictlike
    
    def test_core_type_comparison(self):
        self.assertTrue(isinstance(dict, self.interface))
    
    def test_core_instance_comparison(self):
        self.assertTrue(isinstance(dict(), self.interface))
    
    def test_user_type_comparison(self):
        self.assertTrue(isinstance(UserDict, self.interface))
    
    def test_user_instance_comparison(self):
        self.assertTrue(isinstance(UserDict(), self.interface))
    
    def test_failure(self):
        self.assertFalse(isinstance(object(), self.interface))
