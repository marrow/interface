# encoding: utf-8

import inspect
import warnings


__all__ = [
        'Attribute',
        'Property', 'ClassProperty', 'InstanceProperty',
        'Method', 'ClassMethod', 'StaticMethod'
    ]



class Attribute(object):
    __instance__ = False
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)
    
    def __init__(self, name=None):
        self.name = name
    
    def __call__(self, instance):
        if not hasattr(instance, self.name):
            raise TypeError("Does not meet interface requirements.")
        
        self.check(instance, getattr(instance, self.name))
    
    def check(self, instance, value):
        return


class Property(Attribute):
    def __init__(self, name=None, type=None, validator=None):
        super(Property, self).__init__(name)
        
        self.type = type
        self.validator = validator
    
    def check(self, instance, value):
        super(Property, self).check(instance, value)
        
        if self.type and not isinstance(value, self.type):
            raise TypeError("Does not meet interface requirements.")
        
        if self.validator and not self.validator(value):
            raise TypeError("Does not meet interface requirements.")


class ClassProperty(Property):
    def check(self, instance, value):
        super(ClassProperty, self).check(instance, value)
        
        if not self.name in instance.__dict__:
            raise TypeError("Does not meet interface requirements.")
        
        if self.name not in (cls.__dict__ for cls in type(instance).mro()):
            raise TypeError("Does not meet interface requirements.")


class InstanceProperty(Property):
    __instance__ = True
    
    def check(self, instance, value):
        super(InstanceProperty, self).check(instance, value)
        
        if self.name not in instance.__dict__:
            raise TypeError("Does not meet interface requirements.")


class Method(Attribute):
    def __init__(self, name=None, like=None, args=None, vargs=None, names=tuple(), kwargs=None, optional=tuple()):
        super(Method, self).__init__(name)
        
        if like:
            names, vargs, kwargs, defaults = inspect.getargspec(like)
            args = len(names)
            optional = set(defaults)
        
        self.args = args
        self.names = set(names)
        self.vargs = vargs
        self.kwargs = kwargs
        self.optional = set(optional)
    
    def check(self, instance, value):
        super(Method, self).check(instance, value)
        
        if not inspect.ismethod(value):
            raise TypeError("Does not meet interface requirements.")
        
        names, vargs, kwargs, defaults = inspect.getargspec(value)
        
        if names[0] in ('self', 'cls'):
            del names[0]
        
        if self.args is not None and len(names) < self.args:
            raise TypeError("Does not meet interface requirements.")
        
        if self.names and not set(names) & self.names == self.names:
            raise TypeError("Does not meet interface requirements.")
        
        if self.vargs is not None and self.vargs != vargs:
            raise TypeError("Does not meet interface requirements.")
        
        if self.kwargs is not None and self.kwargs != kwargs:
            raise TypeError("Does not meet interface requirements.")
        
        if self.optional and not set(defaults) & self.optional == self.optional:
            raise TypeError("Does not meet interface requirements.")


class ClassMethod(Method):
    def check(self, instance, value):
        super(ClassMethod, self).check(instance, value)
        
        mro = (instance if inspect.isclass(instance) else type(instance)).mro()
        
        for cls in mro:
            if self.name in cls.__dict__:
                if type(cls.__dict__[self.name]) is classmethod:
                    break
        
        else:
            raise TypeError("Does not meet interface requirements.")


class StaticMethod(Method):
    def check(self, instance, value):
        super(ClassMethod, self).check(instance, value)
        
        mro = (instance if inspect.isclass(instance) else type(instance)).mro()
        
        for cls in mro:
            if self.name in cls.__dict__:
                if type(cls.__dict__[self.name]) is staticmethod:
                    break
        
        else:
            raise TypeError("Does not meet interface requirements.")
