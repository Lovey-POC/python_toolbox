# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `find_clear_place_on_circle`.'''

import pathlib

import nose.tools

from python_toolbox import temp_file_tools

from python_toolbox.misc_tools import add_extension_if_plain


def test():
    assert str(add_extension_if_plain(r'''c:\hello.zip''', '.ogg')) == \
                                                            r'''c:\hello.zip'''
    assert str(add_extension_if_plain(r'''c:\hello''', '.ogg')) == \
                                                            r'''c:\hello.ogg'''
    assert str(add_extension_if_plain(r'''c:\hello''', '.mkv')) == \
                                                            r'''c:\hello.mkv'''