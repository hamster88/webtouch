from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time

from webtouch.task import Task
from webtouch.reporter import Reporter



class Worker():
    def __init__(self, task_cls:type[Task], reporter:Reporter, concurrent=0, min_delay=0, max_delay=0):
        self.task_cls = task_cls
        self.reporter = reporter
        self.concurrent =  concurrent or task_cls.CONCURRENT
        self.min_delay = min_delay or task_cls.MIN_DELAY
        self.max_delay = max_delay or task_cls.MAX_DELAY
        
        
        self.is_picking = False
        self.executor = ThreadPoolExecutor(max_workers=self.concurrent)
        self._thr = threading.Thread(target=self.pickup, daemon=True)

        self.logger = logging.getLogger('worker')
        
    def run_task(self):
        t = self.task_cls()
        t.logger = self.logger.getChild('task')
        self.reporter.begin(t)
        t.run()
        self.reporter.end(t)


    def pickup(self):
        while self.is_picking:
            n = self.executor._work_queue.qsize()
            if n < 1:
                self.executor.submit(self.run_task)
                
            
            
            self.sleep()
    
    def start(self):
        self.logger.info('start worker')
        if self.is_picking:
            self.logger.debug(f'start worker skiped ({self.is_picking=})')
            return

        self.is_picking = True
        self._thr.start()
        self.logger.debug('start worker ok')
        
    
    def stop(self):
        self.logger.info('stop worker')
        if self.executor:
            self.is_picking = False
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            self.logger.debug('stop worker ok')
        else:
            self.logger.debug(f'stop worker skiped ({self.executor=})')
            

    def sleep(self):
        s = self.min_delay
        if self.min_delay < self.max_delay:
            s =  uniform(self.min_delay, self.max_delay)
            
        time.sleep(s)
     