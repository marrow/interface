"""Release information about Marrow Interface."""

from collections import namedtuple


version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(2, 0, 0, 'final', 0)
version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "An anti-Pythonic declarative strict interface definition and validation system."
url = 'https://github.com/marrow/interface/'
