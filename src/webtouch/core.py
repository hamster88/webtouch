

from collections import defaultdict, deque
from queue import Queue
import logging
import threading
import time
import os
import sys


from webtouch import Task, Reporter, Worker


            
# 这样设计可以么
class LogHandler(logging.Handler):
    def __init__(self, handle:callable):
        super().__init__()
        self.handle = handle

    def emit(self, record:logging.LogRecord):
        text = self.format(record) 
        
        if not( self.handle is None ):
            self.handle(text, record)

class Core():
    def __init__(self):
        self.option = defaultdict('')

        self._init_logger()
    
    def _init_logger(self):
        log_format = '%(asctime)s.%(msecs)03d [%(levelname)s]\t%(name)s: %(message)s'
        log_level = logging.DEBUG
        log_datefmt = "%Y-%m-%d %H:%M:%S"

        # 创建日志记录器
        self._name = f'Core.{hex(id(self))[2:]}'
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(log_level)

        # 创建格式化器
        formatter = logging.Formatter(log_format, datefmt=log_datefmt)

        # 添加自定义日志处理器
        log_handler = LogHandler(self.handle_log)
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
         
    # 定义日志处理函数
    def handle_log(self, text: str, record: logging.LogRecord):
        """
        处理日志内容的函数
        :param text: 格式化后的日志内容
        :param record: 日志记录对象
        """
        # 示例:将日志内容打印到控制台(可以自定义存储或处理逻辑)
        print(f"[Custom Log Handler] {text}")
        

    def main(self, task_cls:type[Task]): 
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.worker.start()
        
        # TODO: ...
    
    def viewer(self):
        
        mode = self.option['view']
        self.logger.info(f'start viewer ({mode=})')
        
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




def init_logging():
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
    