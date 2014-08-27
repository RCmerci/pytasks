# -*- coding: utf-8 -*-



class _Infinite(object):
    def __init__(self):
        self._v = 7
    def __eq__(self, v):
        return self._v == v._v
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
    def _oper(op):
        def wrapped_func(self, v):
            self._v = getattr(self._v, op)(v)
            return self
        return wrapped_func
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
    __iadd__ = _oper('__add__')
    __isub__ = _oper('__sub__')
    __imul__ = _oper('__mul__')
    __idiv__ = _oper('__div__')
    __ifloordiv__ = _oper('__floordiv__')

Infinite = _Infinite()

from time import sleep
from functools import wraps
def sleep_before_run(func, sec):
    @wraps
    def wrapped_func():
        sleep(sec)
        func()
    return wrapped_func
