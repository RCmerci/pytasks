# -*- coding: utf-8 -*-
#import pdb
from time import sleep as _sleep
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
from util import Infinite as _infinite
def _add(aim, sec):
    return aim+_timedelta(seconds=sec)
def _now():
    return _datetime.now()

def task1():
    print 'task1'

def task2():
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
task2.schedule = _schedule1
task1.times = _infinite
task2.times = 3
#task1.every = _timedelta(seconds=1)
task2.every = _timedelta(seconds=2) 
