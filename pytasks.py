# -*- coding: utf-8 -*-

import Queue
import time
import threading


worker_list = None
tasksq = Queue.Queue()

def start(threadnum=5):
    global tasksq
    put_init_tasks(tasksq)
    global worker_list
    if not worker_list:
        worker_list = []
    for i in range(threadnum):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()
        worker_list.append(t)
    interaction()


def worker():
    # print 'in func [worker]'
    while 1:
        task_callable = tasksq.get()
        task_callable()
        tasksq.task_done()

    pass


current_user = ''
init_task_file = None
def put_init_tasks(queue_instance):
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
            print init_task_file
        except ImportError:
            print 'no init-task-file found'
            init_task_file = None
            return
    ########### 以上：得到inittasks

    func_list = [func for func in dir(init_task_file)]
    def is_func_or_callable(f):
        if getattr(f, '__call__', None):
            return True
        if 'function' in str(type(f)):
            return True
        return False

    func_list = filter(is_func_or_callable, func_list)
    for func in func_list:
        queue_instance.put(Task([func]))
    del func_list


def interaction():
    def lookup():
        print 'call lookup()'
        print Task.TaskNum
    def NoneFunc():
        print 'not found command'
        pass
    while 1:
        input = raw_input('>')
        locals().get(input, 'NoneFunc')()


class Task(object):
    Schedule = {
        'now':0,
        'every_X':1,
        'default':0,
    }
    Schedule_num = [0, 1]
    TaskNum = 0
    def __init__(self, func_list, schedule=None, interval=None):
        self.func_list = func_list
        self.schedule = Schedule['default']
        if schedule in Schedule_num and interval:
            self.schedule = Schedule[schedule]
            self.interval = int(interval)
        Task.TaskNum += 1
        self.tasknum = Task.TaskNum
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
        while self.schedule:
            for func in self.func_list:
                func()
            time.sleep(self.interval)
    def __repr__(self):
        return '<Task %s>'%(self.tasknum)
    __str__ = __repr__
    def __del__(self):
        Task.TaskNum -= 1


if __name__ == '__main__':
    start()












#####
#  add()
#  delete()
#  start()
#
#
