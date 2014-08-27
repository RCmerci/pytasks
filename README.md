#pytasks
用于执行`例行任务`

###Example-1

```
    #tasks.py是用于test的py文件
    % python pytasks.py
```

###Example-2
*
```
    % vim tasks.py
```
*
```
        #tasks.py   ----do task at 2014-12-12 12:12:00

    from datetime import datetime as _date
    def task():
        ##do-something
        print 'done-work'
    task.schedule = lambda:_date(2014,12,12,12,12)
```
*
```
    %python pytasks.py
```
*
done
### Example-3
```
    #test.py
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
```
