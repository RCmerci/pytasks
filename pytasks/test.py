# -*- coding: utf-8 -*-
from pytasks import App, Infinite
from datetime import datetime as dt
from datetime import timedelta as td
import os

class T:
    def __init__(self, taskid):
        self.times = Infinite
        self.now = dt.now()
        self.taskid = taskid
    def __call__(self):
        print self.taskid, ":", dt.now()-self.now
        self.now =dt.now()
    def schedule(self):
        return dt.now()+td(seconds=2)
task1 = T(1)
task2 = T(2)

task2.schedule = lambda: True if os.environ['LOGNAME']=='rcmerci' else False




app = App()
app.add(task1)
#app.add(task2)

app.run()
