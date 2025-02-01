from __future__ import annotations

from collections import Counter
from itertools import count
import logging
from random import uniform
import time


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
        
        self.logger = logging.getLogger('task')

        
    
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
    def check(cls, reporter):
        '''周期性检查函数'''
        pass


class SleepTask(Task):
    delay = 1
    def __init__(self):
        super().__init__()
        self.delay = uniform(2, 20)
        self.title = f'Sleep_{self.delay:.0f}'
        self.summary = f'Sleep {self.delay} seconds'
        
    def main(self):

        if self.delay > 15:
            raise ValueError('x > 15. (test unknown error)')
        
        self.logger.info(f'start\t{self.id}\t{self.title}')
        time.sleep(self.delay)
        self.logger.info(f'done\t{self.id}\t{self.title}')
        
        if self.delay > 10:
            self.error = 'x > 10 (test error)'
        

        

class FetchTask(Task):
    url:str
    def __init__(self):
        super().__init__()

