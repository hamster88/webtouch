from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time

from webtouch import Task, Reporter

logger = logging.getLogger('worker')
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

    def run_task(self):
        t = self.task_cls()
        self.reporter.begin()
        t.run()
        self.reporter.end()


    def pickup(self):
        while self.is_picking:
            if self.executor._work_queue.qsize() < 1:
                self.executor.submit(self.do_task)
                
            self.sleep()
    
    def start(self):
        logger.info('start worker')
        if self.is_picking:
            logger.debug(f'start worker skiped ({self.is_picking=})')
            return

        self.is_picking = True
        self._thr.start()
        logger.debug('start worker ok')
        
    
    def stop(self):
        logger.info('stop worker')
        if self.executor:
            self.is_picking = False
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            logger.debug('stop worker ok')
        else:
            logger.debug(f'stop worker skiped ({self.executor=})')
            

    def sleep(self):
        s = self.min_delay
        if self.min_delay < self.max_delay:
            s =  uniform(self.min_delay, self.max_delay)
            
        time.sleep(s)
     