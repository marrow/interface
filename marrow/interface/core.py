# encoding: utf-8

import inspect

from marrow.interface.schema import Attribute


__all__ = ['InterfaceMeta', 'Interface']

ALLOWED_PROPERTIES = ('__doc__', '__module__', '__assume_interface__',
    '__qualname__')


class InterfaceMeta(type):
    def __new__(meta, name, bases, attrs):
        # Handle the initial Interface class, which defines no interfaces.
        if len(bases) == 1 and bases[0] is object:
            attrs['__abstract__'] = dict()
            return type.__new__(meta, name, bases, attrs)

        abstract = dict()

        for key in attrs:
            if key in ALLOWED_PROPERTIES:
                continue

            value = attrs[key]

            if not isinstance(value, Attribute):
                raise TypeError("Interfaces must only contain Attribute "
                    "instances, not a %s named %s." % (
                        type(value).__name__, key))

            if value.name is None:
                value.name = key

            abstract[key] = value

        for base in bases:
            if type(base) is not InterfaceMeta:
                raise TypeError(
                    "Do not mix interfaces with other base classes.")

            collision = set(abstract) & set(base.__dict__['__abstract__'])

            if collision:
                raise TypeError("Conflicting interfaces, %s redefines: %s" % (
                        base.__name__, ', '.join(collision)))

            abstract.update(base.__dict__['__abstract__'])

        attrs['__abstract__'] = abstract

        return type.__new__(meta, name, bases, attrs)

    def __instancecheck__(cls, inst, live=True):
        """Does the given instance support this interface?"""
        return cls.implements(inst)

    def implements(interface, instance):
        assumptions = interface.__dict__.get('__assume_interface__', [])

        if inspect.isclass(instance):
            for assumption in assumptions:
                if issubclass(instance, assumption):
                    return True

        else:
            for assumption in assumptions:
                if isinstance(instance, assumption):
                    return True

        for i, j in interface.__abstract__.items():
            if not j(instance):
                return False

        return True


Interface = InterfaceMeta("Interface", (object, ), dict())
