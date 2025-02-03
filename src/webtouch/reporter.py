from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
import logging
from random import uniform
import threading
import time

from webtouch.task import Task

class Reporter():
    def __init__(self, maxlen=32):
        
        self.running:deque[Task] = deque(maxlen=maxlen)
        self.history:deque[Task] = deque(maxlen=maxlen)
        self.invalid:deque[Task] = deque(maxlen=maxlen)
        
        self.counter = Counter()
        self.sheet = Counter()
        self.state = defaultdict(lambda:'')
        
        self.on_begin = lambda: None
        self.on_end = lambda: None
        
    def begin(self, t:Task):
        self.running.append(t)
        self.counter['running'] += 1
        self.counter['total'] += 1
        self.on_begin()
      
    def end(self, t:Task):
        self.running.remove(t)
        self.counter['running'] -= 1
        
        
        if 'invalid' in t.tags:
            self.invalid.append(t)
            self.counter['invalid'] += 1
        else:
            self.history.append(t) 
            self.counter['history'] += 1
            
        self.counter['end'] += 1
        
        self.on_end()
        
