#pytasks
用于执行`例行任务`

###Example-1
```python
    #tasks.py是用于test的py文件
    % python pytasks.py
```

###Example-2
1. ```
    % vim tasks.py
```
2. ```
        tasks.py   ----do task at 2014-12-12 12:12:00

    from datetime import datetime as _date
    def task():
        ##do-something
        print 'done-work'
    task.schedule = lambda:_date(2014,12,12,12,12)
```

3. ```
%python pytasks.py
```
4. #####done
