#!/usr/bin/env python
# encoding: utf-8

import os
import sys

try:
    from setuptools.core import setup, find_packages
except ImportError:
    from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand

if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
    raise SystemExit("Python 3.2 or later is required.")

exec(open(os.path.join("marrow", "interface", "release.py")).read())


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
    
        self.test_args = []
        self.test_suite = True
    
    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


tests_require = ['pytest', 'pytest-cov']

setup(
        name = "marrow.interface",
        version = version,
        
        description = "An anti-Pythonic declarative strict interface definition and validation system.",
        long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.interface""",
        
        author = "Alice Bevan-McGregor",
        author_email = "alice+marrow@gothcandy.com",
        url = "https://github.com/marrow/marrow.interface",
        license = "MIT",
        
        install_requires = [
            'marrow.util < 2.0'
        ],
        
        tests_require = tests_require,
        
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        zip_safe = False,
        include_package_data = True,
        package_data = {'': ['README.textile', 'LICENSE']},
        
        namespace_packages = ['marrow'],
        
        cmdclass = dict(
                test = PyTest,
            )
    )
