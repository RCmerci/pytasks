# -*- coding: utf-8 -*-



class _Infinite(object):
    def __cmp__(self, v):
        if isinstance(v, _Infinite):
            return 0
        return 1
    def __lt__(self, v):
        return False
    def __gt__(self, v):
        if isinstance(v, _Infinite):
            return False
        return True
    def __repr__(self):
        return '<infinite>'
    __str__ = __repr__
    def __sub__(self, v):
        return self
    __add__ = __sub__
    __mul__ = __sub__
    __floordiv__ = __sub__
    __div__ = __sub__
    __radd__ = __sub__
    __rsub__ = __sub__
    __rmul__ = __sub__
    __rdiv__ = __sub__
    __rfloordiv__ = __sub__
    __iadd__ = __sub__
    __isub__ = __sub__
    __imul__ = __sub__
    __idiv__ = __sub__
    __ifloordiv__ = __sub__

Infinite = _Infinite()

from time import sleep
from functools import wraps
def sleep_before_run(func, sec):
    @wraps
    def wrapped_func():
        sleep(sec)
        func()
    return wrapped_func
