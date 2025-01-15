
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time

from webtouch.task import Task

logger = logging.getLogger('worker')


class Worker():
    task_cls:type
    concurrent:int
    delay:float
    delay2:float = 0
    
    executor:ThreadPoolExecutor
    # tasks_running:deque[Task]
    # tasks_history:deque[Task]
    # emit:callable
    
    is_picking = False
    _thr = None
    def __init__(self, task_cls, concurrent=16, delay=0):
        self.task_cls = task_cls
        self.concurrent = concurrent
        # self.emit = emit or pass_emit

        try:
            self.delay = delay[0]
            self.delay2 = delay[1]
        except (TypeError, IndexError, KeyError, AttributeError):
            self.delay = delay
        
        
        
        self.is_picking = False
        self.executor = ThreadPoolExecutor(max_workers=self.concurrent)
        # self.tasks_running = deque(maxlen=self.concurrent)
        # self.tasks_history = deque(maxlen=max(self.concurrent, 32))

    
    def do_task(self):

        t = self.task_cls()
        
        self.tasks_running.append(t)
        # self.emit('worker:submit', (self, t))
        t.start()
        
        self.tasks_running.remove(t)
        self.tasks_history.append(t)
        # self.emit('worker:done', (self, t))
        

    def pickup(self):
        
        while self.is_picking:
            if self.executor._work_queue.qsize() < 1:
                self.executor.submit(self.do_task)

            self.sleep()
    
    def start(self):
        logger.info('start worker thread')
        if self.is_picking:
            logger.debug('already exists worker thread')
            return self._thr
        logger.debug('create worker thread')
        
        self.is_picking = True
        self._thr = threading.Thread(target=self.pickup, daemon=True)
        self._thr.start()
        
        return self._thr
    
    
    def stop(self):
        self.is_picking = False
        self.executor.shutdown(wait=False, cancel_futures=True)
    
    def sleep(self):
        s = self.delay
        if self.delay2:
            s =  uniform(self.delay, self.delay2)
            
        time.sleep(s)
        
