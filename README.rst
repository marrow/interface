================
Marrow Interface
================


    © 2011-2019, Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/interface

..

   |latestversion| |ghtag| |masterstatus| |mastercover| |masterreq| |ghwatch| |ghstar|

.. warning:: This project is no longer Python 2 compatible, and due to the change in how namespace packages are
             packaged this project is directly incompatible with any other project utilizing the ``marrow`` namespace
             that **is** compatible with Python 2. *Always pin your version ranges.*

1. What is Marrow Interface?
============================

Marrow Interface is a light-weight—less than 200 lines of code—flexible, declarative schema system for Python objects.
If you are familiar with Object Relational Mappers (ORMs) or Object Document Mappers (ODMs) then this style of system
should already be familiar.

Marrow Interface provides deep runtime checking of these objects using simple ``isinstance`` calls.  It is encouraged
to check these objects as early as possible in your application's lifespan; the best location, if possible, is during
configuration or startup.  Additionally, if you are writing extensible software, plugins conforming to your API should
not need to be aware of the literal interface at any time other than during unit test execution.

An example of this dependency issue is for a template engine.  The template engine may want to have a helper that
conforms to the API used by a web framework; using other solutions the template engine would need to require the web
framework be installed to declare its support for that API.  This isn't very desirable.

An additional issue is that of double-checking.  The double-check problem is that while an object may declare that it
supports an interface, it can lie.  The consumer (code which uses the object) still has to check before using it, thus
there is no benefit in declaring support for an interface up-front.  The cost for this is the aforementioned reverse
dependancy which when combined with the double-check problem, is needless.

Marrow Interface solves these problems by automating the introspection of an object needed to validate that it does,
in fact, conform to a given API.


1.1. Why Avoid Duck Typing?
---------------------------

Duck typing—where if it walks like a duck (probably does what you expect it to do), talks like a duck (supports an
implicit shared interface), it's probably a duck—is great for core Python APIs such as dictionary access.  This type
of implicit API suffers from a small set of rather significant problems:

* You can only confirm an object does what you want by trying it out.  This means you can't check things ahead of time,
  for example, during configuration versus first use.  This means errors can crop up in unexpected places far removed
  from the last place you had anything to do with a given object.

* You have to handle all sorts of errors: ``AttributeError``, ``TypeError``, and possibly others like ``ValueError``
  and ``NotImplementedError``.  This makes exception handling for exceptions you *expect* a given API to generate more
  difficult, especially considering that raw except blocks (exception handlers that catch anything) are just as likely
  to eat real exceptions raised by bugs or incompatible data.

Duck typing works great if there are no bugs.  There are always bugs.  It also works great if you can have 100% trust
that an object will always be treated a certain way; this kind of trust can only be reliably given to the standard
library.  To be truly safe and robust you have to assume everyone is lying to you.

Most of the `rationale behind Abstract Base Classes <http://www.python.org/dev/peps/pep-3119/>`_ applies here as well.

As a rather off-colour analogy, consider this conversation:

* Boyfriend: "We're going to have fun!"

* Girlfriend: "No we're not."

* Boyfriend: (hurt) "Oh."

Duck typing replicates this conversation every time an attempt to use an object that does not conform to the
specification is used.  It's abrupt, possibly rude, and would be a terrible way to brute-force a conversation in real
life.


1.2. What About Abstract Base Classes or Zope Interface?
--------------------------------------------------------

Abstract Base Classes (ABCs) offer a registry in addition to subclass-based membership.  Because of this:

* Objects which implement an interface must have knowledge of that ABC.  This sets up a reverse dependancy, which is
  problematical for reasons elaborated upon in the next section.

* ABCs are themselves concrete classes.  They aren't truly abstract unlike the more strict definition used by C++ and
  Java.

* You can potentially have metaclass conflicts when subclassing from parent classes with different metaclasses.

* You do not avoid the double-check problem.

To continue the analogy, consider this conversation:

* Boyfriend: "I'd like to have fun!"

* Girlfriend: "Could we have fun?"

* Boyfriend: "I can do that."

Zope Interface (``z.i``) suffers from all the same problems, except for the subclassing issue.  In ``z.i`` you execute
function calls at the class scope to *register* your adherence to an interface.  Zope Interface also has a clear
distinction between class-level implementation of a protocol, and objects which *provide* the interface.



2. Installation
===============

Installing ``marrow.interface`` is easy, just execute the following in a terminal::

    pip install marrow.interface

If you add ``marrow.interface`` to the ``install_requires`` argument of the call to ``setup()`` in your application's
``setup.py`` file, ``marrow.interface`` will be automatically installed and made available when your own application is
installed.  We recommend using "less than" version numbers to ensure there are no unintentional side-effects when
updating.  Use ``marrow.interface<1.1`` to get all bugfixes for the current release, and ``marrow.interface<2.0`` to
get bugfixes and feature updates, but ensure that large breaking changes are not installed.


2.1. Development Version
------------------------

    |developstatus| |developcover| |ghsince| |issuecount| |ghfork|

Development takes place on `GitHub <https://github.com/>`_ in the
`marrow.interface <https://github.com/marrow/interface>`_ project.  Issue tracking, documentation, and downloads
are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`_, a distributed source code management
system.  If you have Git, you can run the following to download and *link* the development version into your Python
runtime::

    git clone https://github.com/marrow/interface.git
    (cd interface; python setup.py develop)

You can upgrade to the latest version at any time::

    (cd interface; git pull; python setup.py develop)

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information, see
`GitHub's documentation <http://help.github.com/>`_.


3. Basic Usage
==============

The use of Marrow Interface requires no support on the part of the producer; objects can be checked for conformance
regardless of any knowledge that they will be examined.

To check an interface, simply use ``isinstance`` a la::

    from marrow.interface.base import IMapping
    from collections import UserDict
    
    assert isinstance(UserDict(), IMapping)


3.1. Declaring an Interface
---------------------------

To declare an interface create a new class which derives from ``Interface`` or another ``Interface`` subclass and
utilize the declarative schema objects.  For example::

    from marrow.interface import Interface
    from marrow.interface.schema import Method
    
    class IMapping(Interface):
        __assume__ = (dict,)
        __getitem__ = Method(args=1)
        __setitem__ = Method(args=2)
        __delitem__ = Method(args=1)

The ``__assume__`` attribute of an ``Interface`` allows you to define an interface that accepts built-in types that can
not be introspected.


3.2. Schema
-----------

The following schema classes are available.

3.2.1.% Attribute
~~~~~~~~~~~~~~~~~

This is the base class for all schema objects and accepts a basic set of validation options.  This simply ensures
that the attribute exists and matches the optional initializer arguments.

===================  ========================================================================================================================
Argument             Description
===================  ========================================================================================================================
``doc=None``         Docstring for this attribute. This is the only argument that can be passed positionally.
``value=NoDefault``  Compare the value of the attribute when checking the interface.
``exact=NoDefault``  Compare the identity (using ``is``) of the attribute.
``validator=None``   A callback, accepting the value to be checked as the only argument, that returns ``True`` if valid, ``False`` otherwise.
===================  ========================================================================================================================

These validation options may seem odd, but they allow you to programatically verify state machines (or state in
general) using interfaces; an unintentional feature we think is kinda neat.

3.2.2. Property(Attribute)
~~~~~~~~~~~~~~~~~~~~~~~~~~

This extends the Attribute checks to include typecasting information, accepting the following additional argument:

============  =============================================
Argument      Description
============  =============================================
``type=None`` The type to check against via ``isinstance``.
============  =============================================

Additionally there are two subclasses of Property that accept no additional arguments:

====================  =====================================================================================
Class                 Description
====================  =====================================================================================
``ClassProperty``     Ensure the property is defined at the class level and not overridden in the instance.
``InstanceProperty``  The inverse of the above; ensure this value is set or overridden in the instance.
====================  =====================================================================================

3.2.3. Callable(Attribute)
~~~~~~~~~~~~~~~~~~~~~~~~~~

This schema class validates the argument specification of a callable.

=================  =================================================================================
Argument           Description
=================  =================================================================================
``like=None``      Copy the argument specification from another callable.
``args=None``      The number of positional arguments.  Absolute; there can be no more and no fewer.
``optional=None``  The number of optional positional arguments.  There may be more.
``names=None``     The names of required keyword arguments.  There may be others.
``vargs=None``     If ``True``, enforces the acceptance of unlimited positional arguments.
``kwargs=None``    If ``True``, enforces the acceptance of unlimited keyword arguments.
=================  =================================================================================

Additionally there are three subclasses of Callable that accept no additional arguments:

================  ================================================================================
Class             Description
================  ================================================================================
``Method``        Ensure the callable is a true class method, e.g. not a lambda or plain function.
``ClassMethod``   A method defined using the ``classmethod`` decorator.
``StaticMethod``  A method defined using the ``staticmethod`` decorator.
================  ================================================================================


4. Version History
==================

Version 1.0
-----------

* Initial release.

Version 1.0.1
-------------

* Corrected issue with Python 3.3, see `issue #2 <https://github.com/marrow/interface/pull/2>`_.

Version 2.0
-----------

* Removed Python 2 compatibility and testing.

* Refactored to use `Marrow Schema <https://github.com/marrow/schema>`_ for the declarative syntax.

* Full test coverage and expanded test capability with improved `Travis-CI <https://travis-ci.org>`_ integration.

* Use of ``__assume_interface__`` is deprecated; this attribute is now called ``__assume__``.

* The ability to define ``__doc__`` docstrings for each schema element has been removed.

* Wheel distribution.


5. Contributors
===============

* `Alice Bevan-McGregor <https://github.com/amcgregor>`_
* `Nando Florestan <https://github.com/nandoflorestan>`_


6. License
==========

Marrow Interface has been released under the MIT Open Source license.


6.1. The MIT License
--------------------

Copyright © 2011-2019 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |ghwatch| image:: https://img.shields.io/github/watchers/marrow/interface.svg?style=social&label=Watch
    :target: https://github.com/marrow/interface/subscription
    :alt: Subscribe to project activity on Github.

.. |ghstar| image:: https://img.shields.io/github/stars/marrow/interface.svg?style=social&label=Star
    :target: https://github.com/marrow/interface/subscription
    :alt: Star this project on Github.

.. |ghfork| image:: https://img.shields.io/github/forks/marrow/interface.svg?style=social&label=Fork
    :target: https://github.com/marrow/interface/fork
    :alt: Fork this project on Github.

.. |masterstatus| image:: http://img.shields.io/travis/marrow/interface/master.svg?style=flat
    :target: https://travis-ci.org/marrow/interface
    :alt: Release Build Status

.. |developstatus| image:: http://img.shields.io/travis/marrow/interface/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/interface
    :alt: Development Build Status

.. |latestversion| image:: http://img.shields.io/pypi/v/marrow.interface.svg?style=flat
    :target: https://pypi.python.org/pypi/marrow.interface
    :alt: Latest Version

.. |downloads| image:: http://img.shields.io/pypi/dw/marrow.interface.svg?style=flat
    :target: https://pypi.python.org/pypi/marrow.interface
    :alt: Downloads per Week

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/interface/master.svg?style=flat
    :target: https://codecov.io/github/marrow/interface?branch=master
    :alt: Release Test Coverage

.. |masterreq| image:: https://img.shields.io/requires/github/marrow/interface.svg
    :target: https://requires.io/github/marrow/interface/requirements/?branch=master
    :alt: Status of release dependencies.

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/interface/develop.svg?style=flat
    :target: https://codecov.io/github/marrow/interface?branch=develop
    :alt: Development Test Coverage

.. |developreq| image:: https://img.shields.io/requires/github/marrow/interface.svg
    :target: https://requires.io/github/marrow/interface/requirements/?branch=develop
    :alt: Status of development dependencies.

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/interface/2.0.0.svg
    :target: https://github.com/marrow/interface/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/interface.svg
    :target: https://github.com/marrow/interface/tree/2.0.0
    :alt: Latest Github tagged release.

.. |issuecount| image:: http://img.shields.io/github/issues/marrow/interface.svg?style=flat
    :target: https://github.com/marrow/interface/issues
    :alt: Github Issues

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
