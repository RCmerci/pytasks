# -*- coding: utf-8 -*-
import pdb
import Queue
import time as _time
import threading
import functools
import heapq
import datetime
import copy

from util import Infinite, sleep_before_run
__all__ = [
    'App',
]

current_user = ''
init_task_file = None

class WorkerList(list):
    def __init__(self, *args, **kargs):
        list.__init__(self, *args, **kargs)
    def workers_info(self):
        pass
class PollList(list):
    def __init__(self, *args, **kargs):
        list.__init__(self, *args, **kargs)
        heapq.heapify(self)
    def pop(self):
        return heapq.heappop(self)
    def push(self, v):
        return heapq.heappush(self, v)
    def heapqify(self):
        heapq.heapify(self)
    def is_empty(self):
        try:
            self.__getitem__(0)
            return False
        except IndexError:
            return True
    def clear_all(self):
        self.__init__()
    def min(self):
        try:
            return self.__getitem__(0)
        except:
            return None
    def max(self):
        try:
            return heapq.nlargest(1, self)[0]
        except:
            return None
    def __contains__(self, v):
        for i in self:
            if i == v:
                return True
        return False

worker_list = WorkerList()
tasksq = Queue.Queue()
poll_list = PollList()

def start(threadnum=5):
    global poll_list
    if not poll_list:
        poll_list = PollList()
    global tasksq
    task_list = put_init_tasks(poll_list)
    global worker_list
    if not worker_list:
        worker_list = WorkerList()
    for i in range(threadnum):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()
        worker_list.append(t)
    poll_t = threading.Thread(target=poll_func)
    poll_t.setDaemon(True)
    poll_t.start()
    inter = Interaction(task_list)
    inter()

def worker(_tasksq=None):
    if not _tasksq:
        global tasksq
    else:
        tasksq = _tasksq
    while 1:
        task_callable = tasksq.get()
        task_callable()
        tasksq.task_done()
def poll_func(poll_l=None):
    if not poll_l:
        global poll_list
        poll_l = poll_list
    temp_poll_list = PollList()
    def polling(tc, should_run, runtime):
        if should_run == False and runtime == Infinite:
            pass
        elif should_run == True and runtime <= datetime.timedelta(0):
            temp_poll_list.push(tc)
            # print 'put task'
            tasksq.put(tc)
        elif should_run == False and runtime < Infinite:
            temp_poll_list.push(tc)
        elif should_run == True and\
             (runtime > datetime.timedelta(0) and\
              Infinite > runtime):
            temp_poll_list.push(tc)
    while 1:
        while not poll_l.is_empty():
            tc = poll_l.pop()
            should_run, runtime = tc.should_run()
            polling(tc, should_run, runtime)

        poll_l = copy.copy(temp_poll_list)
        temp_poll_list.clear_all()
        try:
            sleep_time = max(poll_l.min().nexttime_in_sec, 0)
        except:
            sleep_time = 0.5
        finally:
            _time.sleep(sleep_time)

def put_init_tasks(poll_list, _init_task_file=None, current_user=None):
    """初始化 poll_list"""
    if not _init_task_file:
        global init_task_file
    else:
        init_task_file = _init_task_file
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
                print filter(lambda e:not e.startswith('_'), dir(init_task_file))
        except ImportError:
            print "not found init task file"
            return
    ########### 以上：得到inittasks
    def not_start_with_(f, il):
        return not f.startswith(il)
    func_list = [getattr(init_task_file, func) for func in dir(init_task_file) if not_start_with_(func, '_')]
    def is_func_or_callable(f):
        if hasattr(f, '__call__'):
            return True
        if 'function' in str(type(f)):
            return True
        return False
    func_list = filter(is_func_or_callable, func_list)
    task_list = []
    for func in func_list:
        func_chain = [func]
        t = Task(func_chain)
        poll_list.push(t)
        task_list.append(t)
    return task_list

class Interaction(object):
    def __init__(self, task_list):
        self.task_list = task_list
    def lookup(self):
        print 'call lookup()'
        print 'tasks number: ', len(self.task_list)
        print '-----------------------------'
        print 'task    status  alive times nexttime'
        temp_task_list = []
        for task in self.task_list:
            print task, task.get_status(), '  ', task.alive, '  ', task.times, ' ', task.nexttime
            if not task.is_done():
                temp_task_list.append(task)
        self.task_list = temp_task_list
        del temp_task_list
    def quit(self):
        exit()
    def threads_info(self):
        pass
    def NoneFunc(self):
        print 'not found command'
        pass
    def __call__(self):
        while 1:
            input = raw_input('>')
            input = input.strip(' ,=_-|')
            getattr(self, input, self.NoneFunc)()

class Task(object):
    TaskNum = 0
    Status = {
        'waiting':0,
        'success':1,
        'ongoing':2,
        'done':3,
        'fail':0
    }
    Status_list = ['waiting','success', 'ongoing', 'done', 'fail']
    def __init__(self, func_list):
        self.func_list = func_list
        try:
            self.schedule = func_list[0].schedule
        except AttributeError:
            self.schedule = Task._default_schedule
        try:
            self.times = func_list[0].times
        except AttributeError:
            self.times = 1
        try:
            self._every = func_list[0].every
        except:
            self._every = datetime.timedelta(seconds=5)
        Task.TaskNum += 1
        self.tasknum = Task.TaskNum
        self.status = Task.Status['waiting']
        self.nexttime = datetime.timedelta(seconds=0.5)
        self.lasttime = None
        self._alive = True
        self._totaltime = self.times
        self._succ_fail_stat = 0
        self.should_run = self._should_run(self.should_run)  # add decorator on function should_run
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
        for func in self.func_list:
            self.times -= 1
            try:
                func()
                self._succ_fail_stat += Task.Status['success']
            except:
                self._succ_fail_stat += Task.Status['fail']
            finally:
                if not self.alive:
                    self.status = Task.Status['done']
                self.lasttime = datetime.datetime.now()
    def __repr__(self):
        return '<Task %s>'%(self.tasknum)
    __str__ = __repr__
    @staticmethod
    def _default_schedule():
        return True
    def get_status(self):
        return Task.Status_list[self.status]
    def is_done(self):
        return True if self.status == Task.Status['done'] else False
    def __le__(self, v):
        return self.nexttime <= v.nexttime
    @property
    def nexttime_in_sec(self):
        return self.nexttime.total_seconds()
    def should_run(self):
        """return (should_run,runtime)
        在runtime之后，run or not (true|false)
        """
        try:
            result = self.schedule()
        except:
            # print 'case 1'
            self.times = 0
            self.status = Task.Status['done']
            return False, Infinite
        if not self.alive:
            # print 'case 2'
            self.times = 0
            self.status = Task.Status['done']
            return False, Infinite
        if result == True: #and self.alive:
            # print 'case 3'
            self.nexttime = self._every
            return True, datetime.timedelta(0)
        if result == False: #and self.alive:
            # print 'case 4'
            self.nexttime = self._every
            return False, self.nexttime
        if result <= datetime.datetime.now(): #and self.alive:
            # print 'case 5'
            # self.nexttime != self._every
            # 这里的nexttime应该为 small_interval()
            # 如果不是的话以下情况会不符合要求：
            # self.every > 两次schedule()之差 这里不考虑schedule()返回 bool()
            self.nexttime = datetime.timedelta(seconds=0.1)
            return True, datetime.timedelta(0)
        if result > datetime.datetime.now(): #and self.alive:
            # print 'case 6'
            self.nexttime = result - datetime.datetime.now()
            return True, self.nexttime
        else:
            # print 'case 7'
            raise ScheduleError
    def _should_run(self, should_run):
        self._last_should_run = None
        self._last_runtime = None
        self._last_schedule_time = None
        self._last_times = copy.copy(self.times)
        @functools.wraps(should_run)
        def wrapped_func(*args, **kwargs):
            if self._last_should_run == True and \
               self._last_runtime > datetime.timedelta(0) and\
               self._last_times == self.times:
                interval = datetime.datetime.now() - self._last_schedule_time
                runtime = self._last_runtime - interval
                if runtime > datetime.timedelta(0):
                    # print '1'
                    self.nexttime = runtime
                else:
                    # print '2'
                    # self.nexttime = self._every
                    # 理由同self.should_run 的case 5
                    self.nexttime = datetime.timedelta(seconds=0.01)

                return (True, runtime)
            _should_run, _runtime = should_run(*args, **kwargs)
            self._last_should_run = _should_run
            self._last_runtime = _runtime
            self._last_schedule_time = datetime.datetime.now()
            self._last_times = copy.copy(self.times)
            return (_should_run, _runtime)
        return wrapped_func
    @property
    def alive(self):
        """this task is alive or not"""
        if self.times <= 0:
            self._alive = False
            return False
        else:
            self._alive = True
            return True
    @alive.setter
    def alive(self, v):
        pass
    @property
    def success_time(self):
        return self._succ_fail_stat
    def __eq__(self, v):
        if isinstance(v, Task) and self.tasknum == v.tasknum:
            return True
        return False
class App(object):
    def __init__(self, init_task_file=None, threadnum=5):
        self.worker_list = WorkerList()
        self.poll_list = PollList()
        self.tasksq = Queue.Queue()
        self.threadnum = threadnum
        if init_task_file:
            _unused = put_init_tasks(self.poll_list, init_task_file)
        self.poll_t = App._init_data_structure(self.poll_list, self.tasksq, self.worker_list, self.threadnum)  # poll_t : polling thread
    @staticmethod
    def _init_data_structure(poll_list, tasksq, worker_list, threadnum):
        """
        初始化 poll_list ---> poll_func所轮询的对象
               tasksq -----> worker 线程工作对象
               worker_list --> workers list
        """
        # if not poll_list:
        #     poll_list = PollList()
        #     task_list = put_init_tasks(poll_list)
        # if not worker_list:
        #     worker_list = WorkerList()
        for i in range(threadnum):
            t = threading.Thread(target=worker, args=(tasksq, ))
            t.setDaemon(True)
            # t.start()
            worker_list.append(t)
        poll_t = threading.Thread(target=poll_func, args=(poll_list, ))
        # poll_t.setDaemon(True)
        # poll_t.start()
        return  poll_t
    def _start_threads(self):
        for t in self.worker_list:
            t.start()
        self.poll_t.start()
    def add(self, task_callable):
        self.poll_list.push(Task([task_callable]))
    def run(self):
        self._start_threads()
        self.poll_t.join()


class NotFoundInitFile(Exception):
    __str__ = lambda:"can't find the initial file"
class ScheduleError(Exception):
    __str__ = lambda:"task.schedule return wrong value"

if __name__ == '__main__':
    start()
