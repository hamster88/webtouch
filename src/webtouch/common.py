from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time

from webtouch import Task, Reporter, Worker


logger = logging.getLogger('mypkg')


class App():
    def __init__(self):
        self.logger = logging.Logger() 
        # TODO: 
    
    def main(self, task_cls:type[Task]):
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.worker.start()
        
        # TODO: ...
        
        