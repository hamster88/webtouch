from __future__ import annotations

from collections import defaultdict, deque
from queue import Queue
import logging
import threading
import time
import os
import sys

from webtouch.reporter import Reporter
from webtouch.task import Task
from webtouch.worker import Worker


class LogHandler(logging.Handler):
    def __init__(self, on_log:callable):
        super().__init__()
        self.on_log = on_log

    def emit(self, record:logging.LogRecord):
        if not( self.on_log is None ):

            self.on_log(record)


class Core():
    def __init__(self):
        self.option = defaultdict(lambda:'')
        self.lock = threading.Lock()
        self._init_logger()
    
    def _init_logger(self):
        log_format = '%(asctime)s.%(msecs)03d %(name)s [%(levelname)s] \t %(message)s'
        log_format_short = '%(asctime)s [%(levelname)s] \t %(message)s'
        
        log_level = logging.DEBUG
        log_datefmt = "%Y-%m-%d %H:%M:%S"
        log_datefmt_short = "%H:%M:%S"   
         
        
        # 创建日志记录器
        self._name = f'Core.{hex(id(self))[2:]}'
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(log_level)

        # 创建格式化器
        self._log_formatter = logging.Formatter(log_format, datefmt=log_datefmt)
        self._log_formatter_short = logging.Formatter(log_format_short, datefmt=log_datefmt_short)

        # 添加自定义日志处理器
        log_handler = LogHandler(self.handle_log)
        log_handler.setFormatter(self._log_formatter)
        self.logger.addHandler(log_handler)
         
    # 定义日志处理函数
    def handle_log(self, record: logging.LogRecord):
        
        text = self._log_formatter_short.format(record)
        # 示例:将日志内容打印到控制台(可以自定义存储或处理逻辑)
        with self.lock:
            print(f"{text}")
        

    def main(self, task_cls:type[Task]): 
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.reporter.logger =  self.logger
        self.worker.logger =  self.logger
        self.task_cls.logger = self.logger
        
        self.worker.start()
        
        self.viewer()
    
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
                