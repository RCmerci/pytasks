# -*- coding: utf-8 -*-
import pdb
import Queue
import time as _time
import threading
import functools

if __debug__:
    from sys import getrefcount
class WorkerList(list):
    def __init__(self, *args, **kargs):
        list.__init__(self, *args, **kargs)
    def workers_info(self):


worker_list = None
tasksq = Queue.Queue()

def start(threadnum=5):
    global tasksq
    task_list = put_init_tasks(tasksq)
    global worker_list
    if not worker_list:
        worker_list = WorkerList()
    for i in range(threadnum):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()
        worker_list.append(t)
    inter = Interaction(task_list)
    inter()


def worker():
    # print 'in func [worker]'
    while 1:
        task_callable = tasksq.get()
        task_callable()
        tasksq.task_done()

current_user = ''
init_task_file = None
def put_init_tasks(queue_instance):
    if __debug__:
        print 'in put_init_tasks'
    global init_task_file
    global current_user
    if not current_user:
        import os, sys
        current_user = os.getenv("LOGNAME")
        if not current_user:
            current_user = 'root'
            sys.path.append(os.path.join('/'))  # add sys.path
        sys.path.append(os.path.join('/', 'home', current_user))
    if not init_task_file:
        try:
            import importlib
            import tasks as init_task_file  # tasks.py
            if __debug__:
                print dir(init_task_file)
        except ImportError:
            print 'no init-task-file found'
            init_task_file = None
            return []
    ########### 以上：得到inittasks
    def not_start_with_(f, il):
        return not f.startswith(il)
    func_list = [getattr(init_task_file, func) for func in dir(init_task_file) if not_start_with_(func, '_')]
    # if __debug__:
    #     print func_list
    def is_func_or_callable(f):
        if hasattr(f, '__call__'):
            return True
        if 'function' in str(type(f)):
            return True
        return False
    if __debug__:
        print func_list
    func_list = filter(is_func_or_callable, func_list)
    if __debug__:
        print func_list
    task_list = []
    for func in func_list:
        func_chain = [func]
        t = Task(func_chain, getattr(func, 'schedule', None))
        queue_instance.put(t)
        task_list.append(t)
    return task_list

class Interaction(object):
    def __init__(self, task_list):
        self.task_list = task_list
    def lookup(self):
        print 'call lookup()'
        print 'tasks number: ', len(self.task_list)
        print '-----------------------------'
        temp_task_list = []
        for task in self.task_list:
            print task, task.get_status()
            if not task.is_done():
                temp_task_list.append(task)
        self.task_list = temp_task_list
        # if __debug__:print getrefcount(self.task_list[0])
        del temp_task_list
    def quit(self):
        exit()
    def threads_info(self):

    def NoneFunc(self):
        print 'not found command'
        pass
    def __call__(self):
        while 1:
            input = raw_input('>')
            input = input.strip(' ,=_-|')
            getattr(self, input, 'NoneFunc')()

class Task(object):
    Schedule = {
        'now':0,
        'every_X':1,
        'default':0,
    }
    Schedule_type = [0, 1]
    TaskNum = 0
    Status = {
        'ongoing':0,
        'pending':1,
        'done':2
    }
    Status_list = ['ongoing', 'pending', 'done']
    def __init__(self, func_list, schedule=None, interval=None, time=1):
        self.func_list = func_list
        self.time = time
        self.schedule = Task.Schedule['default']
        if schedule in Task.Schedule_type and interval:
            self.schedule = Task.Schedule[schedule]
            self.interval = int(interval)
        Task.TaskNum += 1
        self.tasknum = Task.TaskNum
        self.status = Task.Status['pending']
    def add_to_tail(self, *func_list):
        """把func_list加到self.func_list 尾
        self.func_list是一个task的函数list"""
        self.func_list.extend(func_list)
    def del_func(self, *func_list):
        """删除self.func_list中在func_list出现的函数"""
        def _del(func):
            return not func in self.func_list

        self.func_list = filter(_del, func_list)
    def __call__(self):
        self.status = Task.Status['ongoing']
        @self._gen_schedule_func()
        def _call():
            for func in self.func_list:
                # pdb.set_trace()  #
                func()
        _call()
        self.status = Task.Status['done']
    def __repr__(self):
        return '<Task %s>'%(self.tasknum)
    __str__ = __repr__
    def __del__(self):
        Task.TaskNum -= 1
    def _gen_schedule_func(self):
        if self.schedule and self.interval:
            schedule = self.schedule
            interval = self.interval
            def schedule_func(func):
                @functools.wraps(func)
                def wraped_func(*args, **kargs):
                    times = self.time
                    while times:
                        func(*args, **kargs)
                        time.sleep(interval)
                        times -= 1
                return wraped_func
        else:
            def schedule_func(func):
                @functools.wraps(func)
                def wraped_func(*args, **kargs):
                    func(*args, **kargs)
                return wraped_func
        return schedule_func
    def get_status(self):
        return Task.Status_list[self.status]
    def is_done(self):
        return True if self.status == Task.Status['done'] else False
if __name__ == '__main__':
    start()
