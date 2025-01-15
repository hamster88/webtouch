

from collections import defaultdict, deque
from queue import Queue
import logging
import threading
import time
import os
import sys


from webtouch import Task, Reporter, Worker

# 现在我想把app模块改写成类，使其能生成多个app实例
# 我不知道后续该怎么做了，感觉非常混乱

# file:  app.py (new code)

class App():
    def __init__(self):
        self.option = defaultdict('')
        
        self.logger = logging.getLogger('App')
    
    def main(self, task_cls:type[Task]):
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.worker.start()
        
        # TODO: ...
        


# file:  app.py (old code)

logger = logging.getLogger()

lq = Queue(maxsize=1024)
ld = deque(maxlen=1024)
lp = lambda:lq.get()

option = defaultdict('')


def main(self, task_cls:type[Task]):
    self.task_cls = task_cls
    
    self.reporter = Reporter(self.task_cls.CONCURRENT)
    self.worker = Worker(self.task_cls, self.reporter)
    
    self.worker.start()
    
    viewer()


def viewer():
    global lp
    
    mode = option['view']
    logger.info(f'start viewer ({mode=})')
    
    if mode == 'adv':
        pass
    
    if mode in ['log', 'debug']:
        try:
            while True:
                input()
        except KeyboardInterrupt:
            pass
        finally:
            os._exit(0)
      
        

def init():
    lformat='%(asctime)s.%(msecs)03d [%(levelname)s]\t%(name)s: %(message)s'
    llevel=logging.DEBUG
    ldatefmt="%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(format=lformat, level=llevel, datefmt=ldatefmt, handlers=[ViewHandler()])
    
    
    

# 自定义日志处理器
class ViewHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record:logging.LogRecord):
        text = self.format(record) 
        lq.put((text, record))


# 消费日志队列
def lconsumer():
    while True:
        lp() # default is lambda:lq.get()


# 直接逐行打印日志
def lprinter():
    text:str
    record:logging.LogRecord
    
    _, s = text.split(' ', 1)
    print(s, file=sys.stdout)


# 缓存近期日志(供高级视图显示)
def lcache():
    text:str
    record:logging.LogRecord
    while not lq.empty():
        ld.append(lq.get())
    