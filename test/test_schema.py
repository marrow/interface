# encoding: utf-8

"""Test the schema objects."""

from unittest import TestCase

from marrow.interface import schema



class TestAttributeSuccesses(TestCase):
    foo = 27
    
    basic = schema.Attribute("basic attribute")
    basic.name = 'basic'
    
    value = schema.Attribute(value=27)
    value.name = 'foo'
    
    exact = schema.Attribute()
    exact.name = 'exact'
    exact.exact = exact
    
    validator = schema.Attribute(validator=lambda v: 20 < v < 30)
    validator.name = 'foo'
    
    def test_basic_repr(self):
        self.assertEqual(repr(self.basic), "Attribute(basic)")
    
    def test_basic_docstring(self):
        self.assertEqual(self.basic.__doc__, "basic attribute")
    
    def test_basic_call(self):
        self.assertTrue(self.basic(self))
    
    def test_value_call(self):
        self.assertTrue(self.value(self))
    
    def test_exact_call(self):
        self.assertTrue(self.exact(self))
    
    def test_validator_call(self):
        self.assertTrue(self.validator(self))


class TestAttributeFailure(TestCase):
    foo = 42
    
    basic = schema.Attribute()
    basic.name = 'bar'
    
    value = schema.Attribute(value=27)
    value.name = 'foo'
    
    exact = schema.Attribute()
    exact.name = 'exact'
    exact.exact = None
    
    validator = schema.Attribute(validator=lambda v: 20 < v < 30)
    validator.name = 'foo'
    
    def test_basic_call(self):
        self.assertFalse(self.basic(self))
    
    def test_value_call(self):
        self.assertFalse(self.value(self))
    
    def test_exact_call(self):
        self.assertFalse(self.exact(self))
    
    def test_validator_call(self):
        self.assertFalse(self.validator(self))


class TestProperty(TestCase):
    foo = 27
    bar = "baz"
    
    good = schema.Property(type=int)
    good.name = 'foo'
    
    bad = schema.Property(type=int)
    bad.name = 'bar'
    
    def test_property_success(self):
        self.assertTrue(self.good(self))
    
    def test_property_failure(self):
        self.assertFalse(self.bad(self))


class TestClassProperty(TestCase):
    foo = 27
    
    good = schema.ClassProperty()
    good.name = 'foo'
    
    bad = schema.ClassProperty()
    bad.name = 'bar'
    
    def __init__(self, *args, **kw):
        super(TestClassProperty, self).__init__(*args, **kw)
        self.bar = 42
    
    def test_class_property_success(self):
        self.assertTrue(self.good(self))
    
    def test_class_property_failure(self):
        self.assertFalse(self.bad(self))


class TestInstanceProperty(TestCase):
    foo = 27
    bar = 42
    
    good1 = schema.InstanceProperty()
    good1.name = 'bar'
    
    good2 = schema.InstanceProperty()
    good2.name = 'baz'
    
    bad = schema.InstanceProperty()
    bad.name = 'foo'
    
    def __init__(self, *args, **kw):
        super(TestInstanceProperty, self).__init__(*args, **kw)
        self.bar = 27
        self.baz = 42
    
    def test_instance_property_override_success(self):
        self.assertTrue(self.good1(self))
    
    def test_instance_property_unique_success(self):
        self.assertTrue(self.good2(self))
    
    def test_instance_property_failure(self):
        self.assertFalse(self.bad(self))


class BaseCallables(object):
    foo = "foo"
    
    def callable1(self, arg1, arg2=None):
        pass
    
    @classmethod
    def callable2(cls, *args, **kw):
        pass
    
    @staticmethod
    def callable3():
        pass


class TestCallableBasics(TestCase, BaseCallables):
    good = schema.Callable()
    good.name = 'callable1'
    
    bad = schema.Callable()
    bad.name = 'foo'
    
    notdictionary = object()
    
    error = schema.Callable()
    error.name = '__getitem__'
    
    def test_callable_base_success(self):
        self.assertTrue(self.good(self))
    
    def test_callable_base_failure(self):
        self.assertFalse(self.bad(self))
    
    def test_callable_introspect_fail(self):
        self.assertFalse(self.error(self.notdictionary))


class TestCallableArgspecSuccess(TestCase, BaseCallables):
    # like=None, args=None, optional=None, names=None, vargs=None, kwargs=None
    
    args = schema.Callable(args=1)
    optional = schema.Callable(optional=1)
    names = schema.Callable(names=('arg1', 'arg2'))
    args.name = optional.name = names.name = 'callable1'
    args.skip = optional.skip = names.skip = 1
    
    vargs = schema.Callable(vargs=True)
    kwargs = schema.Callable(kwargs=True)
    vargs.name = kwargs.name = 'callable2'
    vargs.skip = kwargs.skip = 1
    
    like_basic = schema.Callable(like=BaseCallables.callable1)
    like_basic.name = 'callable1'
    
    like_variable = schema.Callable(like=BaseCallables.callable2)
    like_variable.name = 'callable2'
    
    like_override = schema.Callable(like=BaseCallables.callable1, args=2)
    like_override.name = 'callable1'
    
    def test_callable_args(self):
        self.assertTrue(self.args(self))
    
    def test_callable_optional(self):
        self.assertTrue(self.optional(self))
    
    def test_callable_names(self):
        self.assertTrue(self.names(self))
    
    def test_callable_vargs(self):
        self.assertTrue(self.vargs(self))
    
    def test_callable_kwargs(self):
        self.assertTrue(self.kwargs(self))
    
    def test_callable_like_basic(self):
        self.assertTrue(self.like_basic(self))
    
    def test_callable_like_variable(self):
        self.assertTrue(self.like_variable(self))
    
    def test_callable_like_override(self):
        self.assertTrue(self.like_override(self))


class TestCallableArgspecFailures(TestCase, BaseCallables):
    # like=None, args=None, optional=None, names=None, vargs=None, kwargs=None
    
    args = schema.Callable(args=1)
    optional = schema.Callable(optional=1)
    names = schema.Callable(names=('arg1', 'arg2'))
    args.name = optional.name = names.name = 'callable2'
    args.skip = optional.skip = names.skip = 1
    
    vargs = schema.Callable(vargs=True)
    kwargs = schema.Callable(kwargs=True)
    vargs.name = kwargs.name = 'callable1'
    vargs.skip = kwargs.skip = 1
    
    like_basic = schema.Callable(like=BaseCallables.callable1)
    like_basic.name = 'callable2'
    
    like_variable = schema.Callable(like=BaseCallables.callable2)
    like_variable.name = 'callable1'
    
    def test_callable_args(self):
        self.assertFalse(self.args(self))
    
    def test_callable_optional(self):
        self.assertFalse(self.optional(self))
    
    def test_callable_names(self):
        self.assertFalse(self.names(self))
    
    def test_callable_vargs(self):
        self.assertFalse(self.vargs(self))
    
    def test_callable_kwargs(self):
        self.assertFalse(self.kwargs(self))
    
    def test_callable_like_basic(self):
        self.assertFalse(self.like_basic(self))
    
    def test_callable_like_variable(self):
        self.assertFalse(self.like_variable(self))


class TestMethod(TestCase, BaseCallables):
    good1 = schema.Method()
    good1.name = 'callable1'
    
    good2 = schema.Method()
    good2.name = 'callable1'
    
    bad = schema.Method()
    bad.name = 'callable3'
    
    def test_method_success(self):
        self.assertTrue(self.good1(self))
    
    def test_class_method_success(self):
        self.assertTrue(self.good2(self))
    
    def test_method_failure(self):
        self.assertFalse(self.bad(self))


class TestClassMethod(TestCase, BaseCallables):
    good = schema.ClassMethod()
    good.name = 'callable2'
    
    bad1 = schema.ClassMethod()
    bad1.name = 'callable1'
    
    bad2 = schema.ClassMethod()
    bad2.name = 'callable3'
    
    def test_class_method_success(self):
        self.assertTrue(self.good(self))
    
    def test_method_failure(self):
        self.assertFalse(self.bad1(self))
    
    def test_static_method_failure(self):
        self.assertFalse(self.bad2(self))


class TestStaticMethod(TestCase, BaseCallables):
    good = schema.StaticMethod()
    good.name = 'callable3'
    
    bad1 = schema.StaticMethod()
    bad1.name = 'callable1'
    
    bad2 = schema.StaticMethod()
    bad2.name = 'callable2'
    
    invalid = schema.StaticMethod(args=1)
    invalid.name = 'callable3'
    
    def test_static_method_success(self):
        self.assertTrue(self.good(self))
    
    def test_method_failure(self):
        self.assertFalse(self.bad1(self))
    
    def test_class_method_failure(self):
        self.assertFalse(self.bad2(self))
    
    def test_static_method_parent_failure(self):
        self.assertFalse(self.invalid(self))
