""" Parts of this module are taken from ``pyramid.compat`` module
"""
import sys
import types


# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3
if PY3: # pragma: no cover
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes
    long = int
    def is_nonstr_iter(v):
        if isinstance(v, str):
            return False
        return hasattr(v, '__iter__')
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    long = long
    def is_nonstr_iter(v):
        return hasattr(v, '__iter__')


def text_(s, encoding='latin-1', errors='strict'):
    """  This function is a copy of ``pyramid.compat.text_``

    If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s # pragma: no cover

def bytes_(s, encoding='latin-1', errors='strict'):
    """ This function is a copy of ``pyramid.compat.bytes_``

    If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, text_type): # pragma: no cover
        return s.encode(encoding, errors)
    return s
