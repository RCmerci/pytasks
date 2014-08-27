#pytasks
用于执行`例行任务`
###INSTALL
```
    pip install pytasks
```
### Example
```
    #test.py
    from pytasks import App
    from datetime import datetime as dt
    from datetime import timedelta as td
    class T:
        def __init__(self):
            self.times = 10    #<--------------task 最多执行次数
            self.now = dt.now()
            self.every = td(seconds=4)  #<------task被轮询的频率
        def __call__(self):    #<--------------task执行的具体内容
            print dt.now()-self.now
            self.now =dt.now()
        def schedule(self):    #<--------------task的执行计划：
            return dt.now()+td(seconds=2)         #可返回bool()或datetime.datetime(...)[代表具体执行时刻]
    task = T()                                    #返回bool()时，按self.every频率轮询

    app = App()
    app.add(task)
    app.run()
```
`BSD license`
