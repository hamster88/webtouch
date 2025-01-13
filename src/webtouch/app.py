from collections import defaultdict
import logging
import os
from queue import Queue
import sys
import threading
import time
from webtouch import worker
from webtouch import task

logger = logging.getLogger()

option = defaultdict(lambda:None)
ref_worker = worker.Worker(task.SleepTask)

lq = Queue(maxsize=1024)
lp = lambda s:None

def lconsumer():
    text:str
    record:logging.LogRecord
    
    while True:
        text, record =  lq.get()
        lv = option['log-level'] or logging.INFO
        
        if lv > record.levelno:
            continue
        
        _, s = text.split(' ', 1)
        lp(s)
        

def main():
    global ref_worker
    
    init()
    
    logger.info('init app')

    logger.info('start log consumer thread')
    lp_thr = threading.Thread(target=lconsumer, daemon=True)
    lp_thr.start()
    
    logger.info('init worker')
    w = worker.Worker(task.SleepTask)
    w.emit = emit
    w.start()
    
    ref_worker = w

    viewer()
    
    #w.stop()


def viewer():
    mode = option['view'] or 'tui'
    logger.info(f'start viewer ({mode=})')
    
    if mode == 'tui':
        pass
    if mode == 'counter':
        pass
    if mode == 'overview':
        pass
    if option['view'] in ['log', 'debug']:
        try:
            while True:
                input()
        except KeyboardInterrupt:
            pass
        finally:
            os._exit(0)
      
        

def init():
    global lp
    
    if option['view'] in ['log', 'debug']:
        lp = print_err
    
    if option['view'] == 'debug':
        option['log-level'] = logging.DEBUG
    
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
        



def print_err(s):
    print(s, file=sys.stderr)




def emit(event, data):
    w:worker.Worker
    t:task.Task
    if event == 'worker:submit':
        w, t = data
        #set_state('tasks_running', w.tasks_running)
    if event == 'worker:done':
        w, t = data

