import inspect

from marrow.schema import Container, Attribute as Setting


undefined = object()


class Attribute(Container):
	value = Setting(default=undefined)
	exact = Setting(default=undefined)
	validator = Setting(default=None)
	
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self.__name__)
	
	def __call__(self, instance):
		value = getattr(instance, self.__name__, undefined)
		
		if ( value is undefined ) or \
			( self.value is not undefined and value != self.value ) or \
			( self.exact is not undefined and value is not self.exact ) or \
			( self.validator and not self.validator(value) ) or \
			( not self.check(instance, value) ):
			return False
		
		return True
	
	def check(self, instance, value):
		"""Basic "attribute exists" check; if we get this far, it exists."""
		return True


class Property(Attribute):
	type = Setting(default=None)
	
	def check(self, instance, value):
		if not super(Property, self).check(instance, value) or \
			( self.type and not isinstance(value, self.type) ):
			return
		
		return True


class ClassProperty(Property):
	def check(self, instance, value):
		if not super(ClassProperty, self).check(instance, value) or \
			self.__name__ in instance.__dict__ or \
			self.__name__ not in (attr for cls in type(instance).mro() for attr in cls.__dict__):
			return
		
		return True


class InstanceProperty(Property):
	def check(self, instance, value):
		if not super(InstanceProperty, self).check(instance, value) or \
			self.__name__ not in instance.__dict__:
			return
		
		return True


class Callable(Attribute):
	skip = 0
	
	args = Setting(default=None)
	optional = Setting(default=None)
	names = Setting(default=None)
	vargs = Setting(default=None)
	kwargs = Setting(default=None)
	
	def __init__(self, *args, **kw):
		if 'like' in kw:
			like = kw.pop('like')
		elif args:
			args = list(args)
			like = args.pop(0)
		else:
			like = None
		
		super(Callable, self).__init__(*args, **kw)
		
		if like:
			names_, vargs, kwargs, defaults, *remainder = inspect.getfullargspec(like)
			
			if not self.optional:
				self.optional = len(defaults) if defaults else None
			
			if not self.args and self.names is not None:
				self.args = len(names_) - self.skip - (self.optional or 0)
			
			if not self.names:
				self.names = names_[self.skip:]
		
		self.names = set(self.names) if self.names else None
	
	def check(self, instance, value):
		if not super(Callable, self).check(instance, value) or \
			not hasattr(value, '__call__'):
			return
		
		try:
			names, vargs, kwargs, defaults, *remainder = inspect.getfullargspec(value)
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
			if self.__name__ in cls.__dict__:
				if type(cls.__dict__[self.__name__]) is classmethod:
					return True


class StaticMethod(Callable):
	def check(self, instance, value):
		if not super(StaticMethod, self).check(instance, value):
			return
		
		for cls in (instance if inspect.isclass(instance) else type(instance)).mro():
			if self.__name__ in cls.__dict__:
				if type(cls.__dict__[self.__name__]) is staticmethod:
					return True
				
				break
