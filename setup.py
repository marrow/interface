#!/usr/bin/env python
# encoding: utf-8

import sys
import os

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "interface", "release.py")).read())


setup(
    name="marrow.interface",
    version=version,
    
    description="An anti-Pythonic declarative strict interface definition and validation system.",
    author="Alice Bevan-McGregor",
    author_email="alice+marrow@gothcandy.com",
    url="https://github.com/marrow/marrow.interface",
    download_url="http://pypi.python.org/pypi/marrow.interface",
    license="MIT",
    keywords="",
    
    test_suite="nose.collector",
    tests_require=["nose", "coverage"],
    
    classifiers=[
        "Development Status :: 4 - Beta",
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
    
    packages=find_packages(exclude=["examples", "tests"]),
    zip_safe=True,
    include_package_data=True,
    package_data={
        "": ["README.textile", "LICENSE", "distribute_setup.py"]
    },
    
    namespace_packages=["marrow"]
)