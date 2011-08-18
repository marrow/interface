# encoding: utf-8

import inspect

__all__ = [
        'Attribute',
        'Property', 'ClassProperty', 'InstanceProperty',
        'Method', 'ClassMethod', 'StaticMethod'
    ]



class NoDefault(object):
    pass


class Attribute(object):
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)
    
    # Note: do not use value and exact positionally; they should be keyword only.
    def __init__(self, doc=None, value=NoDefault, exact=NoDefault, validator=None):
        if doc is not None:
            self.__doc__ = doc
        
        self.name = None
        self.value = value
        self.exact = exact
        self.validator = validator
    
    def __call__(self, instance):
        value = getattr(instance, self.name, NoDefault)
        
        if ( value is NoDefault ) or \
           ( self.value is not NoDefault and value != self.value ) or \
           ( self.exact is not NoDefault and value is not self.exact ) or \
           ( self.validator and not self.validator(value) ) or \
           ( not self.check(instance, value) ):
            return False
        
        return True
    
    def check(self, instance, value):
        """Basic "attribute exists" check; if we get this far, it exists."""
        return True


class Property(Attribute):
    def __init__(self, doc=None, type=None, **kw):
        super(Property, self).__init__(doc, **kw)
        
        self.type = type
    
    def check(self, instance, value):
        if not super(Property, self).check(instance, value) or \
           ( self.type and not isinstance(value, self.type) ):
            return
        
        return True


class ClassProperty(Property):
    def check(self, instance, value):
        if not super(ClassProperty, self).check(instance, value) or \
           self.name in instance.__dict__ or \
           self.name not in (attr for cls in type(instance).mro() for attr in cls.__dict__):
            return
        
        return True


class InstanceProperty(Property):
    def check(self, instance, value):
        if not super(InstanceProperty, self).check(instance, value) or \
           self.name not in instance.__dict__:
            return
        
        return True


class Callable(Attribute):
    skip = 0
    
    def __init__(self, doc=None, like=None, args=None, optional=None, names=None, vargs=None, kwargs=None, **kw):
        super(Callable, self).__init__(doc, **kw)
        
        if like:
            names_, vargs, kwargs, defaults = inspect.getargspec(like)
            optional = optional if optional else (len(defaults) if defaults else None)
            args = args if args is not None and names is None else (len(names_) - self.skip - (optional if optional is not None else 0))
            names = names if names is not None else names_[self.skip:]
        
        self.args = args
        self.optional = optional
        self.names = set(names) if names else None
        self.vargs = vargs
        self.kwargs = kwargs
    
    def check(self, instance, value):
        if not super(Callable, self).check(instance, value) or \
           not hasattr(value, '__call__'):
            return
        
        try:
            names, vargs, kwargs, defaults = inspect.getargspec(value)
        except:
            return
        
        if not names:
            names = []
        
        optional = len(defaults) if defaults else 0
        
        del names[:self.skip]
        
        if ( self.args is not None and (len(names) - optional) != self.args ) or \
           ( self.names and not set(names) & self.names == self.names ) or \
           ( self.vargs and not vargs ) or \
           ( self.kwargs and not kwargs ) or \
           ( self.optional is not None and optional != self.optional ):
            return
        
        return True


class Method(Callable):
    skip = 1
    
    def check(self, instance, value):
        if not super(Method, self).check(instance, value) or \
           ( not inspect.isclass(instance) and not inspect.ismethod(value) ):
            return
        
        return True


class ClassMethod(Method):
    def check(self, instance, value):
        if not super(ClassMethod, self).check(instance, value):
            return
        
        mro = (instance if inspect.isclass(instance) else type(instance)).mro()
        
        for cls in mro:
            if self.name in cls.__dict__:
                if type(cls.__dict__[self.name]) is classmethod:
                    return True


class StaticMethod(Callable):
    def check(self, instance, value):
        if not super(StaticMethod, self).check(instance, value):
            return
        
        for cls in (instance if inspect.isclass(instance) else type(instance)).mro():
            if self.name in cls.__dict__:
                if type(cls.__dict__[self.name]) is staticmethod:
                    return True
                
                break
