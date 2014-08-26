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

def task2():
    print 'task2'

def _sche():
    yield _add(_now(),5)
    yield _add(_now(),9)
    yield True
    raise Exception
_schedule1 = _sche().next

def _schedule2():
    return _datetime.now()
task1.schedule = _schedule1
task2.schedule = _schedule2
task1.times = 10
task2.times = 3
task1.every = _timedelta(seconds=1)
task2.every = _timedelta(seconds=2)
