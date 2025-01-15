from collections import defaultdict, deque
import logging
import os
from queue import Empty, Queue
import sys
import threading
import time
from webtouch import worker
from webtouch import task

logger = logging.getLogger()

option = defaultdict(lambda:None)
ref_worker = worker.Worker(task.SleepTask)

lq = Queue(maxsize=1024)
ld = deque(maxlen=1024)
lp = lambda:lq.get()



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
    global lp
    
    mode = option['view'] or 'tui'
    logger.info(f'start viewer ({mode=})')
    
    if mode == 'tui':
        pass
    if mode == 'counter':
        pass
    if mode == 'overview':
        lp = loverviewer
        try:
            while True:
                input()
        except KeyboardInterrupt:
            pass
        finally:
            os._exit(0)
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
        lp = lprinter
    
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


# 消费日志队列
def lconsumer():
    while True:
        lp() # default is lambda:lq.get()


# 逐行打印日志
def lprinter():
    text:str
    record:logging.LogRecord
    
    text, record =  lq.get()
    lv = option['log-level'] or logging.INFO
    
    if lv > record.levelno:
        return
    
    _, s = text.split(' ', 1)
    print(s, file=sys.stdout)


# 每秒打印一次近期日志总结
def loverviewer():
    text:str
    record:logging.LogRecord
    while not lq.empty():
        ld.append(lq.get())
    
    n = 10
    submit_logs = deque(maxlen=n)
    done_logs = deque(maxlen=n)
    warning_logs = deque(maxlen=n)
    
    last_counter = ''
    last_submit = ''
    
    for text, record in ld:
        asctime = record.asctime.split(' ', 1)[-1]
        msg = record.message
        if record.levelno == logging.INFO:
            # action = '@submit '
            # if msg.startswith(action):
            #     item = f'{asctime} ' + msg[len(action):]
            #     submit_logs.append(item)
            # action = '@done '
            # if msg.startswith(action):
            #     item = f'{asctime} ' + msg[len(action):]
            #     done_logs.append(item)    
            
            pass
        
        if record.levelno >= logging.WARNING:
            warning_logs.append(msg)
            
    ref_worker.tasks_running
    ref_worker.tasks_history
    
    # TODO：
        
    
    print('\n'.join(warning_logs))
    print('------------')
    
    # print('\n'.join(done_logs))
    # print('------------')
    # print('\n'.join(submit_logs))
    # print('------------')

    
    time.sleep(1)





def emit(event, data):
    w:worker.Worker
    t:task.Task
    if event == 'worker:submit':
        w, t = data
        logger.info(f'@submit -> {t.title}')
        #set_state('tasks_running', w.tasks_running)
        # print(f'@submit --> {t.title}')
        
    if event == 'worker:done':
        w, t = data
        # print(f'@done <-- {t.title}')
        logger.info(f'@done <- {t.title}')
        

