from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time
from __future__ import annotations

logger = logging.getLogger('mypkg')

class Task:
    CONCURRENT = 16
    MIN_DELAY = 1
    MAX_DELAY = 0
    
    _counter = Counter()
    def __init__(self):
        cls = self.__class__
        self.id = Task._counter[cls]
        self.tid = Task._counter[Task]
        
        Task._counter[cls] += 1
        Task._counter[Task] += 1
        
        self.title = f'{cls.__name__}:{self.tid}'
        self.detail = 'The task is ready.'
        
        self.tags = {'ready'}
        
        
    
    def main(self):
        '''任务主要逻辑'''
        msg = 'function "main" must be implemented by Task subclasses.'
        raise NotImplementedError(msg)
    
    def free(self):
        '''资源清理'''
        pass
    
    def run(self):
        '''安全运行任务单元'''
        
        try:
            self.tags.add('running')
            self.tags.remove('ready')
            self.main()
        except Exception as e:
            self.detail = f'Abort in task: {self.title}\n  {self.detail}\n  {e}'
            self.tags.add('abort')
            self.tags.add('error')
        finally:
            self.tags.add('done')
            self.tags.remove('running')
            self.free()

    @classmethod
    def check(cls, reporter:Reporter):
        '''周期性检查函数'''
        pass


class Reporter():
    def __init__(self, maxlen=32):
        
        self.running:deque[Task] = deque(maxlen=maxlen)
        self.history:deque[Task] = deque(maxlen=maxlen)
        self.invalid:deque[Task] = deque(maxlen=maxlen)
        
        self.counter = Counter()
        self.state = defaultdict('')
        
    def begin(self, t:Task):
        self.running.append(t)
        self.counter['running'] += 1
        self.counter['total'] += 1
        
      
    def end(self, t:Task):
        self.running.remove(t)
        self.counter['running'] -= 1
        
        
        if 'invalid' in t.tags:
            self.errors.append(t)
            self.counter['invalid'] += 1
        else:
            self.history.append(t) 
            self.counter['history'] += 1
            
        self.counter['done'] += 1
        


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
        


class App():
    def __init__(self):
        pass
    
    def main(self, task_cls:type[Task]):
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.worker.start()
        
        # TODO: ...
        
        