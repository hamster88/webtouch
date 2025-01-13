from collections import Counter
from itertools import count
import logging
from random import uniform
import time

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
        self.delay = uniform(20, 50)
        self.title = f'Sleep_{self.delay:.0f}'
        self.summary = f'Sleep {self.delay} seconds'
        
    def run(self):
        logger.info(f'start\t{self.id}\t{self.title}')
        time.sleep(self.delay)
        logger.info(f'done\t{self.id}\t{self.title}')
        

class FetchTask(Task):
    url:str
    def __init__(self):
        super().__init__()

