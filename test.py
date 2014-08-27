# -*- coding: utf-8 -*-
from pytasks import App
from datetime import datetime as dt
from datetime import timedelta as td

class T:
    def __init__(self):
        self.times = 10
        self.now = dt.now()
    def __call__(self):
        print dt.now()-self.now
        self.now =dt.now()
    def schedule(self):
        return dt.now()+td(seconds=2)
task = T()

app = App()
app.add(task)


app.run()
