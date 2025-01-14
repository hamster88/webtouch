from collections import Counter
from itertools import count
import logging
from random import uniform
import time

from webtouch import app

logger = logging.getLogger('task')


class Task:
    id:int = 0
    tid:int = 0
    title:str = ''
    summary:str = ''
    
    _counters = Counter()

    def __init__(self):
        cls = self.__class__
        self.id = Task._counters[cls]
        self.tid = Task._counters['tid']
        Task._counters[cls] += 1
        Task._counters['tid'] += 1
    
    def run(self):
        msg = 'function "run" must be implemented by Task subclasses.'
        raise NotImplementedError(msg)
    
    def start(self):
        try:
            self.run()
        except Exception as e:
            self.error = f'Abort in task: {self.summary}\n{e}'
    
    


class SleepTask(Task):
    delay = 1
    def __init__(self):
        super().__init__()
        self.delay = uniform(2, 20)
        self.title = f'Sleep_{self.delay:.0f}'
        self.summary = f'Sleep {self.delay} seconds'
        
    def run(self):
        if self.delay > 15:
            raise ValueError('x > 15. (test unknown error)')
        
        logger.info(f'start\t{self.id}\t{self.title}')
        time.sleep(self.delay)
        logger.info(f'done\t{self.id}\t{self.title}')
        
        if self.delay > 10:
            self.error = 'x > 10 (test error)'
        

        

class FetchTask(Task):
    url:str
    def __init__(self):
        super().__init__()

