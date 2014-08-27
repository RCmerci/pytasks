# -*- coding: utf-8 -*-
#import pdb
from time import sleep as _sleep
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta

def _add(aim, sec):
    return aim+_timedelta(seconds=sec)
def _now():
    return _datetime.now()

def task1():
    print 'task1'

def _task2():
    print 'task2'

def _sche():
    yield _add(_now(),5)
    yield _add(_now(),9)
    yield True
    raise Exception
_schedule1 = _sche().next

def _schedule2():
    return _datetime.now()+_timedelta(seconds=2)
task1.schedule = _schedule2
_task2.schedule = _schedule2
task1.times = 10
_task2.times = 3
#task1.every = _timedelta(seconds=1)
_task2.every = _timedelta(seconds=2) 
